import sys
import PriorSampling as ps
from copy import deepcopy
from random import random
from numpy import prod
import itertools


class HiddenMarkovModel:
    def __init__(self, event_sequence):
        self.T = event_sequence
        self.init_p = [0.5, 0.5]
        self.transitional_p = [[0.7, 0.3],
                               [0.3, 0.7]]
        self.emission_p = [[0.4, 0.4, 0.2],
                           [0.1, 0.45, 0.45]]

        print("init_p: ", self.init_p)
        print("transitional_p: ", self.transitional_p)
        print("emission_p: ", self.emission_p)

    def forwards(self):
        # 1. Initialisation:
        event = self.convert_value_to_index(self.T[0])
        p_sequence = []
        for index in range(0, len(self.emission_p)):
            p_sequence.append((self.init_p[index] * self.emission_p[index][event]))
        print("p sequence: ", p_sequence)

        # 2. Recursion:
        for current_event_index in range(1, len(self.T)):  # for each event in sequence
            p_sequence_next = []
            for i in range(0, len(p_sequence)):  # For each possible transition state (Heater at t-1)
                p_sequence_recursive = []
                for j in range(0, len(self.init_p)):
                    p_sequence_recursive.append(p_sequence[j] * self.transitional_p[i][j] * self.emission_p[i][self.convert_value_to_index(self.T[current_event_index])])
                p_sequence_next.append(sum(p_sequence_recursive))  # sum
            p_sequence = deepcopy(p_sequence_next)
            print(p_sequence)

        # 3. Termination:
        return sum(p_sequence)

    def convert_value_to_index(self, value):
        if value == "H":
            return 0
        elif value == "W":
            return 1
        else:
            return 2

if __name__ == "__main__":
    event_sequence = ["C", "W", "H", "W", "C"]
    HMM = HiddenMarkovModel(event_sequence)
    # HMM.forwards()
    probability = HMM.forwards()
    print("\nFor event: ", event_sequence, "\nThe probability is: ", probability)