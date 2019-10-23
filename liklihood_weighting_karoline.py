import sys
import PriorSampling as psl
import copy

class likelihoodWeighting():
    def __init__(self):
        ##### USER MAY CHANGE THESE VARIABLES
        self.N = 10000 #number of samples
        self.ps = psl.PriorSampling("sprinkler") #specify which network to use (burglary, sprinkler...)
        self.query_variable = 'R'
        self.evidence = ['+c','+w']
        #####

    def Sample(self):
        query_outcomes = ["+"+self.query_variable.lower(),"-"+self.query_variable.lower()]
        weighted_counts = {query_outcomes[0]:0,query_outcomes[1]:0} # weighted counts initialised to zero
        for n in range(0,self.N):
            [x,w] = self.WeightedSample() #fetch a new sample
            weighted_counts[x[self.query_variable]] += w #update the weight
        #normalise:
        wcounts_sum = float(weighted_counts[query_outcomes[0]])+ float(weighted_counts[query_outcomes[1]])
        normalised_w = copy.deepcopy(weighted_counts)
        normalised_w[query_outcomes[0]] = float(weighted_counts[query_outcomes[0]]) / wcounts_sum
        normalised_w[query_outcomes[1]] = float(weighted_counts[query_outcomes[1]]) / wcounts_sum
        #final output:
        print(normalised_w)

    def WeightedSample(self):
        #initialise return variables
        w = 1
        x = {}
        #format evidence as a dictionary to simplify access
        evidence_dict = {char:sign for sign, char in self.evidence}
        #loop over every node in the net (in top down order)
        for node in self.ps.CPTs["order"]:
            #Determine the value of parent nodes
            parents = self.ps.CPTs["parents"][node]
            parent_outcome = ""
            if not parents == None:
                for parent in parents.split(","):
                    parent_outcome += x[parent]

            #If the value of the current variable is part of the evidence, simply find the value and conditional probability:
            if node.lower() in evidence_dict.keys():
                x[node] = evidence_dict[node.lower()] + node.lower() #write the value to x
                if parents == None:
                    conditional = x[node]
                else:
                    conditional = x[node]+"|"+parent_outcome
                w = w * self.ps.CPTs[node][conditional] #multiply the conditional probability in with w

            #If the value of the current variable is not known/fixed, sample from its CPT:
            else:
                if parents == None:
                    conditional = node.lower()
                else:
                    conditional = node.lower()+"|"+parent_outcome
                x[node] = self.ps.sampleVariable(self.ps.CPTs[node], conditional)
        return x,w

if __name__ == "__main__":
    lw = likelihoodWeighting()
    lw.Sample()