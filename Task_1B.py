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
        self.LUCAS0["parents"] ={"S":   ["YF", "A", "PP"],
                                 "YF":  [None],
                                 "A":   [None],
                                 "PP":  [None],
                                 "G":   [None],
                                 "AD":  ["G"],
                                 "B":   [None],
                                 "CA":  ["AD", "F"],
                                 "F":   ["C", "LC"],
                                 "AL":  [None],
                                 "C":   ["AL", "LC"],
                                 "LC": ["G", "S"]}
        self.create_cpts()

    def create_cpts(self):
        for variable in self.LUCAS0["order"]:
            self.LUCAS0[variable] = {}
            # 1. if no parents its just +/- the variable
            if self.LUCAS0["parents"][variable][0] is None:
                self.LUCAS0[variable]["+" + variable.lower()] = 0
                self.LUCAS0[variable]["-" + variable.lower()] = 0
            else:
                for j in ["+", "-"]:
                    for possible_prob in list(itertools.product([True, False], repeat=(len(self.LUCAS0["parents"][variable])))):
                        prob_lookup = j + variable.lower() + "|"
                        for i in range(0, len(possible_prob)):
                            if possible_prob[i] == True:
                                prob_lookup += "+" + self.LUCAS0["parents"][variable][i].lower()
                            else:
                                prob_lookup += "-" + self.LUCAS0["parents"][variable][i].lower()
                        self.LUCAS0[variable][prob_lookup] = 0

    def parameter_learning(self):
        f = open("lucas0_text/lucas0_test.data", "r")
        self.LUCAS0["order_param_learn"] = {}
        for variable in self.LUCAS0["order"]:
            if variable != "LC":
                self.LUCAS0["order_param_learn"][variable] = 0
        print(self.LUCAS0["order_param_learn"])

        # assign current line to "order_param_learn"
        for line in f:
            print(line)
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            for i in range(0, len(line)):
                current_variable = self.LUCAS0["order"][i]
                self.LUCAS0["order_param_learn"][current_variable] = line[i]
            print(self.LUCAS0["order_param_learn"])

        # Loop through each CPT and add to sum if current state == CPT state.
            for variable in self.LUCAS0["order_param_learn"]:
                print(variable)
                for cpt in self.LUCAS0[variable]:
                    print(cpt)
            # print(line)
            # for current_variable in self.LUCAS0["order"]:
            #     print(self.LUCAS0[current_variable])
            #

            # for variable in line:
            #     print(variable)
            # variable
            # pass

if __name__ == "__main__":
    task = task_1b()
    task.parameter_learning()
    # task.parameter_learning()