import sys
import PriorSampling as ps
from copy import deepcopy
from random import random
from numpy import prod
class gibbsSampling:
    def __init__(self):
        self.N = 10000  # number of samples
        self.psl = ps.PriorSampling("sprinkler")  # Specify which Bayes Net  to use (burglary, sprinkler...)
        self.query_variable = 'S'
        self.evidence_variables = ['+c', '-w']  # Must be in order.
        self.evidence_dict = {char: sign for sign, char in self.evidence_variables}
        self.current_state = []

    def gibbs_ask(self):
        print(self.current_state)
        weight_counts = {"+": 0, "-": 0}
        normalised_w = deepcopy(weight_counts)

        self.current_state = self.generate_initial_sate()  # 1. Generate initial state (x) with random values for the nonevidence variables (Z)

        for i in range(0, self.N):        # 2. For each non-evidence variable (Zi) in non-evidence variable list
            self.sample_new_state()
            # print(self.current_state[self.query_variable])
            # print("+" + self.query_variable.lower())
            if self.current_state[self.query_variable] == "+" + self.query_variable.lower():
                weight_counts["+"] += 1
            else:
                weight_counts["-"] += 1

        print("Final weighted counts: ", weight_counts)
        weight_count_sum = weight_counts["+"] + weight_counts["-"]  # 3. normalise count variable
        normalised_w["+"] = weight_counts["+"] / weight_count_sum
        normalised_w["-"] = weight_counts["-"] / weight_count_sum
        print("normalised_w: ", normalised_w)

    def sample_new_state(self):
        for variable in self.current_state:
            if variable.lower() not in self.evidence_dict:
                parents = []
                children = []
                childrens_parents = []
                prob_parent = 1
                prob_children_list = []

                parents_test = self.psl.CPTs["parents"][variable]  # 1. Find parents:
                if parents_test != None:
                    lookup_prob_parent = self.current_state[variable] + "|"
                    if lookup_prob_parent.find('+') != -1:  # flip the query variable's current state (if + turn it to - vice versa)
                        index = lookup_prob_parent.find('+')
                        lookup_prob_parent = lookup_prob_parent[:index] + '-' + lookup_prob_parent[(index + 1):]
                    else:
                        index = lookup_prob_parent.find('-')
                        lookup_prob_parent = lookup_prob_parent[:index] + '+' + lookup_prob_parent[(index + 1):]

                    for parent in self.psl.CPTs["parents"][variable].split(","):  # get the rest of the lookup probability for the parents:
                        lookup_prob_parent += self.current_state[parent]
                        parents.append(parent)
                    prob_parent = self.psl.CPTs[variable][lookup_prob_parent]

                # 2. for every child find the prob of it's parents.
                for j in range(0, len(self.psl.CPTs["order"])):  # 2. Find children
                    if variable in str(self.psl.CPTs["parents"][self.psl.CPTs["order"][j]]):
                        children.append(str(self.psl.CPTs["order"][j]))

                if children == []:  # if no children - prob = 1?
                    prob_children = 1
                else:
                    # find the children's parents for prob calc:
                    for j in children:  # 3. Find children's other parents.
                        childs_parents_string = self.psl.CPTs["parents"][j]
                        for parent in childs_parents_string.split(","):
                            childrens_parents.append(parent)
                        lookup_prob_children = self.current_state[j] + "|"
                        for child in childrens_parents:
                            lookup_prob_children += self.current_state[child]

                        prob_children_list.append(self.psl.CPTs[j][lookup_prob_children])
                prob_of_change = prob_parent * prod(prob_children_list)

                random_number = random()  # Finally calc if the state of the non_evidence variable should change:
                if random_number < prob_of_change: # flip
                    if self.current_state[variable] == ("+" + variable.lower()):
                        self.current_state[variable] = "-" + variable.lower()
                    else:
                        self.current_state[variable] = "+" + variable.lower()

    def generate_initial_sate(self):
        initial_state = {}
        for variable in self.psl.CPTs["order"]:
            if variable.lower() in self.evidence_dict:
                initial_state[variable] = self.evidence_dict[variable.lower()] + variable.lower()
            else:
                if random() > 0.5:
                    initial_state[variable] = "+" + variable.lower()
                else:
                    initial_state[variable] = "-" + variable.lower()
        return initial_state

if __name__ == "__main__":
    lw = gibbsSampling()
    lw.gibbs_ask()