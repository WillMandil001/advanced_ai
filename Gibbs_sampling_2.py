import sys
import PriorSampling as ps
from copy import deepcopy
from random import random

class gibbsSampling:
    def __init__(self):
        self.N = 10000  # number of samples
        self.psl = ps.PriorSampling("sprinkler")  # Specify which Bayes Net  to use (burglary, sprinkler...)
        self.query_variable = 'R'
        self.evidence_variables = ['+c', '+w']  # Must be in order.
        self.evidence_dict = {char: sign for sign, char in self.evidence_variables}

    def gibbs_ask(self):
        current_state = self.generate_initial_sate()
        print(current_state)

        # if its a nonevidence variable find markov blanket


    def find_markov_blanket(self, ):


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