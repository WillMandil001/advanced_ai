import sys
import PriorSampling as ps
from copy import deepcopy
from random import random
from numpy import prod
import itertools


class BayesianNetwork:
    def __init__(self):
        self.LUCAS0 = {}
        self.LUCAS0["order"] = ["S", "YF", "A", "PP", "G", "AD", "B", "CA", "F", "AL", "C", "LC"]
        self.LUCAS0["order_param_learn"] = {"S": 0, "YF": 0, "A": 0, "PP": 0, "G": 0, "AD": 0, "B": 0, "CA": 0, "F": 0,
                                            "AL": 0, "C": 0, "LC": 0}
        self.LUCAS0["parents"] = {"S": ["A", "PP"],
                                  "YF": ["S"],
                                  "A": [None],
                                  "PP": [None],
                                  "G": [None],
                                  "AD": ["G"],
                                  "B": [None],
                                  "CA": ["AD", "F"],
                                  "F": ["C", "LC"],
                                  "AL": [None],
                                  "C": ["AL", "LC"],
                                  "LC": ["G", "S"]}
        self.create_cpts()
        self.parameter_learning()

    def create_cpts(self):
        for variable in self.LUCAS0["order"]:
            self.LUCAS0[variable] = {}
            # 1. if no parents its just +/- the variable
            if self.LUCAS0["parents"][variable][0] is None:
                self.LUCAS0[variable]["+" + variable.lower()] = 0
                self.LUCAS0[variable]["-" + variable.lower()] = 0
            else:  # 2. If parents:
                for j in ["+", "-"]:
                    for possible_prob in list(
                            itertools.product([True, False], repeat=(len(self.LUCAS0["parents"][variable])))):
                        prob_lookup_list = []
                        prob_lookup = j + variable.lower() + "|"
                        prob_lookup_list.append(j + variable.lower())
                        for i in range(0, len(possible_prob)):
                            if possible_prob[i] == True:
                                prob_lookup += "+" + self.LUCAS0["parents"][variable][i].lower()
                                prob_lookup_list.append("+" + self.LUCAS0["parents"][variable][i].lower())
                            else:
                                prob_lookup += "-" + self.LUCAS0["parents"][variable][i].lower()
                                prob_lookup_list.append("-" + self.LUCAS0["parents"][variable][i].lower())
                        prob_lookup_list.append(0)
                        self.LUCAS0[variable][prob_lookup] = prob_lookup_list

    def parameter_learning(self):
        f = open("lucas0_train.csv", "r")
        content = f.readlines()
        content = content[1:]
        self.LUCAS0["order_param_learn"] = {}
        for variable in self.LUCAS0["order"]:
            self.LUCAS0["order_param_learn"][variable] = 0

        for line in content:  # assign current line to "order_param_learn"
            line = line.replace(',', '').replace('\n', '')
            for i in range(0, len(line)):
                current_variable = self.LUCAS0["order"][i]
                self.LUCAS0["order_param_learn"][current_variable] = line[i]

            for variable in self.LUCAS0[
                "order_param_learn"]:  # Loop through each CPT and add to sum if current state == CPT state.
                if self.LUCAS0["parents"][variable][0] == None:
                    if self.LUCAS0["order_param_learn"][variable] == "1":
                        self.LUCAS0[variable][("+" + variable.lower())] += 1
                    else:
                        self.LUCAS0[variable][("-" + variable.lower())] += 1
                else:  # If the variable does have parents: so there are conditions that need to be calc'd:
                    for cpt_probability in self.LUCAS0[variable]:
                        try:
                            for current_variable in self.LUCAS0[variable][cpt_probability]:
                                if type(current_variable) != int:
                                    if current_variable[0] == "+" and self.LUCAS0["order_param_learn"][
                                        current_variable[1:].upper()] == "0":
                                        raise
                                    if current_variable[0] == "-" and self.LUCAS0["order_param_learn"][
                                        current_variable[1:].upper()] == "1":
                                        raise
                            self.LUCAS0[variable][cpt_probability][-1] += 1
                        except:
                            pass

        # Normalise the data:
        for i in self.LUCAS0["order_param_learn"]:
            sum = 0
            indicator = 0
            for j in self.LUCAS0[i]:
                try:  # 1. For no parents:
                    sum += self.LUCAS0[i][j]
                    indicator = 1
                except:  # 2. if parents:
                    for other_cpt_prob in self.LUCAS0[i]:
                        if other_cpt_prob[0][0] == "+":
                            if self.LUCAS0[i][other_cpt_prob][1:-1] == self.LUCAS0[i][j][1:-1] and \
                                    self.LUCAS0[i][other_cpt_prob][0] != self.LUCAS0[i][j][0]:
                                sum = float(self.LUCAS0[i][other_cpt_prob][-1]) + float(self.LUCAS0[i][j][-1])
                                self.LUCAS0[i][other_cpt_prob][-1] = self.LUCAS0[i][other_cpt_prob][-1] / sum
                                self.LUCAS0[i][j][-1] = self.LUCAS0[i][j][-1] / sum
                                break
            if indicator == 1:
                for j in self.LUCAS0[i]:
                    self.LUCAS0[i][j] = float(self.LUCAS0[i][j])
                    self.LUCAS0[i][j] = self.LUCAS0[i][j] / sum


class RejectionSampling():
    def __init__(self, LUCAS0):
        self.CPTs = LUCAS0
        self.CPTs["order"] = ["A", "PP", "S", "YF", "G", "LC", "AD", "B", "AL", "C", "F", "CA"]  # Re-order for sampling
        for i in self.CPTs["order"]:
            print(self.CPTs[i])

    def sampleVariable(self, CPT, conditional):
        sampledValue = None
        randnumber = random()
        try:
            value1 = CPT["+" + conditional][-1]
        except:
            value1 = CPT["+" + conditional]
        if randnumber < value1:
            sampledValue = "+" + conditional
        else:
            sampledValue = "-" + conditional
        return sampledValue.split("|")[0]

    def sampleVariables(self):
        event = []
        sampledVars = {}
        for variable in self.CPTs["order"]:
            evidence = ""
            conditional = ""
            parents = self.CPTs["parents"][variable]
            if parents[0] == None:
                conditional = variable.lower()
            else:
                for parent in parents:
                    evidence += sampledVars[parent]
                conditional = variable.lower() + "|" + evidence
            sampledValue = self.sampleVariable(self.CPTs[variable], conditional)
            event.append(sampledValue)
            sampledVars[variable] = sampledValue
        return event

    def rejectionSampling(self, number_of_samples, query_event):
        prob_true = 0
        prob_false = 0
        query_variable = query_event.split("|")[0]
        evidence_variables = query_event.split("|")[1].split(",")

        for sample in range(0, number_of_samples):
            event = sampling.sampleVariables()
            if all(elem in event for elem in evidence_variables) == True:
                if query_variable in event:
                    prob_true += 1
                else:
                    prob_false += 1
        print("prob_true = ", prob_true, "prob_false = ", prob_false)

        # Normalise:
        normalised_prob = {}
        normalised_prob["+"] = (prob_true / (prob_true + prob_false))
        normalised_prob["-"] = (prob_false / (prob_true + prob_false))
        return normalised_prob, query_event


class LikelihoodWeighting():
    def __init__(self, LUCAS0, number_of_samples, query_event):
        self.query_event = query_event
        self.CPTs = LUCAS0
        self.N = number_of_samples  # number of samples
        self.query_variable = query_event.split("|")[0][1:].upper()
        self.evidence_variables = query_event.split("|")[1].split(",")  # Must be in order.
        self.evidence_dict = {char: sign for sign, char in self.evidence_variables}

    def sample(self):
        weight_counts = {"+": 0, "-": 0}
        normalised_w = deepcopy(weight_counts)
        for i in range(0, self.N):  # loop for number of samples
            x, w = self.weighted_sample()  # gather query variable event and its associated weight.
            if x == "+":  # for the returned sample add the weight to previous weight sum for this event
                weight_counts[x] += w
            else:
                weight_counts[x] += w
        # normalise:
        weight_count_sum = weight_counts["+"] + weight_counts["-"]
        normalised_w["+"] = weight_counts["+"] / weight_count_sum
        normalised_w["-"] = weight_counts["-"] / weight_count_sum
        return normalised_w, self.query_event

    def sampleVariable(self, CPT, conditional):
        sampledValue = None
        randnumber = random()
        try:
            value1 = CPT["+" + conditional][-1]
        except:
            value1 = CPT["+" + conditional]
        if randnumber < value1:
            sampledValue = "+" + conditional
        else:
            sampledValue = "-" + conditional
        return sampledValue.split("|")[0]

    def weighted_sample(self):
        w = 1
        x = {}
        for variable in self.CPTs["order"]:
            parents = self.CPTs["parents"][variable]

            if variable.lower() in self.evidence_dict:  # if its a evidence variable, calc weights
                x[variable] = self.evidence_dict[variable.lower()] + variable.lower()
                if parents[0] == None:
                    w *= self.CPTs[variable][x[variable]]
                else:
                    query_event_lookup = self.evidence_dict[variable.lower()] + variable.lower() + "|"
                    for parent in parents:
                        query_event_lookup += x[parent]
                    w *= self.CPTs[variable][query_event_lookup][-1]
            else:  # if not an evidence variable then create the sample event from conditional prob table
                if parents[0] == None:
                    conditional_lookup = variable.lower()
                else:
                    conditional_lookup = variable.lower() + "|"
                    for parent in parents:
                        conditional_lookup += (x[parent.upper()])
                x[variable] = self.sampleVariable(self.CPTs[variable], conditional_lookup)
        return x[self.query_variable][0], w


class GibbsAsk:
    def __init__(self, LUCAS0, number_of_samples, query_event):
        self.query_event = query_event
        self.CPTs = LUCAS0
        self.N = number_of_samples  # number of samples
        self.query_variable = query_event.split("|")[0][1:].upper()
        self.evidence_variables = query_event.split("|")[1].split(",")  # Must be in order.
        self.evidence_dict = {char: sign for sign, char in self.evidence_variables}
        self.current_state = []

    def gibbs_ask(self):
        weight_counts = {"+": 0, "-": 0}
        normalised_w = deepcopy(weight_counts)
        self.current_state = self.generate_initial_sate()  # 1. Generate initial state (x) with random values for the nonevidence variables (Z)

        for i in range(0, self.N):  # 2. For each non-evidence variable (Zi) in non-evidence variable list
            self.sample_new_state()
            if self.current_state[self.query_variable] == "+" + self.query_variable.lower():
                weight_counts["+"] += 1
            else:
                weight_counts["-"] += 1

        weight_count_sum = weight_counts["+"] + weight_counts["-"]  # 3. normalise count variable
        normalised_w["+"] = weight_counts["+"] / weight_count_sum
        normalised_w["-"] = weight_counts["-"] / weight_count_sum
        return normalised_w, self.query_event

    def sample_new_state(self):
        for variable in self.CPTs["order"]:
            print("current_state = ", self.current_state)
            prob_parents = 1
            prob_parents_change = 0
            prob_children_parents = 1
            if variable.lower() not in self.evidence_dict:
                print("variable: ", variable)

                # 1. Find the variables parents:
                parents = self.CPTs["parents"][variable]
                if parents[0] is not None:  # if variable has parents we need to calc the P(xi | parents(Xi))
                    current_parents_lookup = self.current_state[variable] + "|"
                    for parent in parents:
                        current_parents_lookup += self.current_state[parent]
                    prob_parents = self.CPTs[variable][current_parents_lookup][-1]
                print("prob_parents: ", prob_parents)

                # 2. Find the variables children:
                children = []
                for v in self.CPTs["order"]:
                    parents = self.CPTs["parents"][v]
                    for i in parents:
                        if i == variable:
                            children.append(v)
                print("children: ", children)

                # 3. find children's parents and product their probabilities:
                prob_children_parents_list = []
                for child in children:
                    child_lookup_prob = self.current_state[child] + "|"
                    for parent in self.CPTs["parents"][child]:
                        if parent != None:
                            child_lookup_prob += self.current_state[parent]
                    prob_children_parents_list.append(self.CPTs[child][child_lookup_prob][-1])
                if prob_children_parents_list:
                    prob_children_parents = prod(prob_children_parents_list)
                print("prob_children_parents: ", prob_children_parents)

                total_prob = prob_parents * prob_children_parents
                print("total_prob: ", total_prob)

                # 4. normalise:

                # 5. randomly sample current variable based on total_pob (P(xi | mb(Xi))):
                random_number = random()  # Finally calc if the state of the non_evidence variable should change:
                if random_number < total_prob:  # flip
                    print("FLIIPPPPPPEEEDDDD!!!!!!!!!!")
                    if self.current_state[variable] == ("+" + variable.lower()):
                        self.current_state[variable] = "-" + variable.lower()
                    else:
                        self.current_state[variable] = "+" + variable.lower()
            print("-----------")

    def generate_initial_sate(self):
        initial_state = {}
        for variable in self.CPTs["order"]:
            if variable.lower() in self.evidence_dict:
                initial_state[variable] = self.evidence_dict[variable.lower()] + variable.lower()
            else:
                if random() > 0.5:
                    initial_state[variable] = "+" + variable.lower()
                else:
                    initial_state[variable] = "-" + variable.lower()
        return initial_state


if __name__ == "__main__":
    task = BayesianNetwork()
    sampling = RejectionSampling(task.LUCAS0)
    query_event = "+s|+c,+f"

    # Calc prob of query event with rejection sampling | event evidence variables should be split with a ","
    normalised_prob, query_event = sampling.rejectionSampling(number_of_samples=10000, query_event=query_event)
    print("From rejection sampling: ", query_event[1:], " = ", normalised_prob)

    # Calc prob of query event with likelihood weighting | event evidence variables should be split with a ","
    likelihood = LikelihoodWeighting(LUCAS0=task.LUCAS0, number_of_samples=10000, query_event=query_event)
    normalised_prob, query_event = likelihood.sample()
    print("From likelihood weighting: ", query_event[1:], " = ", normalised_prob)

    # # Calc prob of query event with likelihood weighting | event evidence variables should be split with a ","
    # gibbs_ask = GibbsAsk(LUCAS0=task.LUCAS0, number_of_samples=1, query_event=query_event)
    # normalised_prob, query_event = gibbs_ask.gibbs_ask()
    # print("From Gibbs Ask: ", query_event[1:], " = ", normalised_prob)
