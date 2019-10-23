import sys
import PriorSampling as ps
from copy import deepcopy


class likelihoodWeighting():
    def __init__(self):
        self.N = 10000  # number of samples
        self.psl = ps.PriorSampling("sprinkler")  # Specify which Bayes Net  to use (burglary, sprinkler...)
        self.query_variable = 'R'
        self.evidence_variables = ['+c','+w']  # Must be in order.
        self.evidence_dict = {char: sign for sign, char in self.evidence_variables}

    def sample(self):
        weight_counts = {"+":0, "-":0}
        normalised_w = deepcopy(weight_counts)
        for i in range (0, self.N):  # loop for number of samples
            x, w = self.weighted_sample()  # gather query variable event and its associated weight.
            if x == "+":  # for the returned sample add the weight to previous weight sum for this event
                weight_counts[x] += w
            else:
                weight_counts[x] += w
        #normalise:
        weight_count_sum = weight_counts["+"] + weight_counts["-"]
        normalised_w["+"] = weight_counts["+"] / weight_count_sum
        normalised_w["-"] = weight_counts["-"] / weight_count_sum
        print(normalised_w)

    def weighted_sample(self):
        w = 1
        x = {}
        for variable in self.psl.CPTs["order"]:
            parents = self.psl.CPTs["parents"][variable]

            if variable.lower() in self.evidence_dict:  # if its a evidence variable, calc weights
                x[variable] = self.evidence_dict[variable.lower()] + variable.lower()
                if parents == None:
                    w *= self.psl.CPTs[variable][x[variable]]
                else:
                    query_event_lookup = self.evidence_dict[variable.lower()] + variable.lower() + "|"
                    for parent in parents.split(","):
                        query_event_lookup += x[parent]
                    w *= self.psl.CPTs[variable][query_event_lookup]
            else:  # if not an evidence variable then create the sample event from conditional prob table
                if parents == None:
                    conditional_lookup = variable.lower()
                else:
                    conditional_lookup = variable.lower()+"|"
                    for parent in parents.split(","):
                        conditional_lookup += (x[parent.upper()])
                x[variable] = self.psl.sampleVariable(self.psl.CPTs[variable], conditional_lookup)
        return x[self.query_variable][0], w

if __name__ == "__main__":
    lw = likelihoodWeighting()
    lw.sample()
