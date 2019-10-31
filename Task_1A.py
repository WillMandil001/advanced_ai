import sys
import PriorSampling as ps
from copy import deepcopy
from random import random
from numpy import prod

class task_1a:
    def __init__(self, pd, ptd, pntnd):
        self.input_variable = {}
        self.input_variable["+d"] = pd
        self.input_variable["+t|+d"] = ptd
        self.input_variable["-t|-d"] = pntnd

    def bayes_theorum_solution(self):
        top_layer = self.input_variable["+t|+d"] * self.input_variable["+d"]
        bottom_layer = top_layer + ( (1 - self.input_variable["-t|-d"]) * (1 - self.input_variable["+d"]))
        pdt = top_layer / bottom_layer
        return pdt

if __name__ == "__main__":
    task = task_1a(pd = 0.0001, ptd = 0.9, pntnd = 0.1)
    print("P(d | t) = ", str(task.bayes_theorum_solution()))