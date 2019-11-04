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
        self.LUCAS0["order_param_learn"] = {"S": 0, "YF": 0, "A": 0, "PP": 0, "G": 0, "AD": 0, "B": 0, "CA": 0, "F": 0, "AL": 0, "C": 0, "LC": 0}
        self.LUCAS0["parents"] ={"S":  ["YF", "A", "PP"],
                                 "YF": [None],
                                 "A":  [None],
                                 "PP": [None],
                                 "G":  [None],
                                 "AD": ["G"],
                                 "B":  [None],
                                 "CA": ["AD", "F"],
                                 "F":  ["C", "LC"],
                                 "AL": [None],
                                 "C":  ["AL", "LC"],
                                 "LC": ["G", "S"]}
        self.create_cpts()
        self.parameter_learning()
        # for i in self.LUCAS0["order_param_learn"]:
        #     print(self.LUCAS0[i])

    def create_cpts(self):
        for variable in self.LUCAS0["order"]:
            self.LUCAS0[variable] = {}
            # 1. if no parents its just +/- the variable
            if self.LUCAS0["parents"][variable][0] is None:
                self.LUCAS0[variable]["+" + variable.lower()] = 0
                self.LUCAS0[variable]["-" + variable.lower()] = 0
            else:  # 2. If parents:
                for j in ["+", "-"]:
                    for possible_prob in list(itertools.product([True, False], repeat=(len(self.LUCAS0["parents"][variable])))):
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
        f = open("lucas0_text/lucas0_train.data", "r")
        self.LUCAS0["order_param_learn"] = {}
        for variable in self.LUCAS0["order"]:
            self.LUCAS0["order_param_learn"][variable] = 0

        # find data for LC:
        f2 = open("lucas0_text/lucas0_train.targets", "r")
        LC_data = []
        for line in f2:
            line = line.replace(' ', '').replace('\n', '')
            if line == "-1": line = "0"
            LC_data.append(line)

        for line, LC_state in zip(f, LC_data):  # assign current line to "order_param_learn"
            line = line.replace(' ', '').replace('\n', '')

            self.LUCAS0["order_param_learn"]["LC"] = LC_state
            for i in range(0, len(line)):
                current_variable = self.LUCAS0["order"][i]
                self.LUCAS0["order_param_learn"][current_variable] = line[i]

            for variable in self.LUCAS0["order_param_learn"]:  # Loop through each CPT and add to sum if current state == CPT state.
                if self.LUCAS0["parents"][variable][0] == None:
                    if self.LUCAS0["order_param_learn"][variable] == "1":
                        self.LUCAS0[variable][("+" + variable.lower())] += 1
                    else:
                        self.LUCAS0[variable][("-" + variable.lower())] += 1
                else:   # If the variable does have parents: so there are conditions that need to be calc'd:
                    for cpt_probability in self.LUCAS0[variable]:
                        try:
                            for current_variable in self.LUCAS0[variable][cpt_probability]:
                                if type(current_variable) != int:
                                    if current_variable[0] == "+" and self.LUCAS0["order_param_learn"][current_variable[1:].upper()] == "0":
                                        raise
                                    if current_variable[0] == "-" and self.LUCAS0["order_param_learn"][current_variable[1:].upper()] == "1":
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
                            if self.LUCAS0[i][other_cpt_prob][1:-1] == self.LUCAS0[i][j][1:-1] and self.LUCAS0[i][other_cpt_prob][0] != self.LUCAS0[i][j][0]:
                                sum = float(self.LUCAS0[i][other_cpt_prob][-1]) + float(self.LUCAS0[i][j][-1])
                                self.LUCAS0[i][other_cpt_prob][-1] = self.LUCAS0[i][other_cpt_prob][-1] / sum
                                self.LUCAS0[i][j][-1] = self.LUCAS0[i][j][-1] / sum
                                break
            if indicator == 1:
                for j in self.LUCAS0[i]:
                    self.LUCAS0[i][j] = float(self.LUCAS0[i][j])
                    self.LUCAS0[i][j] = self.LUCAS0[i][j] / sum


class RejectionSample():
    def __init__(self, LUCAS0):
        self.CPTs = LUCAS0
        self.CPTs["order"] = ["YF", "A", "PP", "S", "G", "LC", "AD", "B", "AL", "C", "F", "CA"]  # Re-order for sampling

    def sampleVariable(self, CPT, conditional):
        sampledValue = None
        randnumber = random()
        try:
            value1 = CPT["+" + conditional][-1]
            value2 = CPT["-" + conditional][-1]
        except:
            value1 = CPT["+" + conditional]
            value2 = CPT["-" + conditional]
        if randnumber <= value1:
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


if __name__ == "__main__":
    task = BayesianNetwork()
    sampling = RejectionSample(task.LUCAS0)
    for i in range(0, 10):
        print("esamplinvent", sampling.sampleVariables())
