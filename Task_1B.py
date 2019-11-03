import sys
import PriorSampling as ps
from copy import deepcopy
from random import random
from numpy import prod
import itertools

class task_1b:
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
        for i in self.LUCAS0["order_param_learn"]:
            print(self.LUCAS0[i])

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
        f = open("lucas0_text/lucas0_test.data", "r")
        self.LUCAS0["order_param_learn"] = {}
        for variable in self.LUCAS0["order"]:
            if variable != "LC":
                self.LUCAS0["order_param_learn"][variable] = 0

        for line in f:  # assign current line to "order_param_learn"
            line = line.replace(' ', '').replace('\n', '')
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

        for i in self.LUCAS0["order_param_learn"]:  # Normalise data:
            sum= 0
            for j in self.LUCAS0[i]:
                try:
                    sum += self.LUCAS0[i][j][-1]
                except:
                    sum += self.LUCAS0[i][j]
            for j in self.LUCAS0[i]:
                if sum == 0:
                    self.LUCAS0[i][j][-1] = 1 / len(self.LUCAS0[i])
                else:
                    try:
                        self.LUCAS0[i][j][-1] = float(self.LUCAS0[i][j][-1])
                        self.LUCAS0[i][j][-1] = self.LUCAS0[i][j][-1] / sum
                    except:
                        self.LUCAS0[i][j] = float(self.LUCAS0[i][j])
                        self.LUCAS0[i][j] = self.LUCAS0[i][j] / sum


if __name__ == "__main__":
    task = task_1b()
