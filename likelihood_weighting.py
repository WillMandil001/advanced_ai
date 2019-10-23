import sys
import random

class PriorSampling:
	CPTs={}

	def __init__(self, netID):
		self.initialiseNet(netID)		

	def initialiseNet(self, netID):
		if netID == "burglary":
			self.CPTs["B"]={"+b":0.001, "-b":0.999}
			self.CPTs["E"]={"+e":0.002, "-e":0.998}
			self.CPTs["A"]={"+a|+b+e":0.95, "-a|+b+e":0.05, 
					"+a|+b-e":0.94, "-a|+b-e":0.06,
					"+a|-b+e":0.29, "-a|-b+e":0.71,
					"+a|-b-e":0.001, "-a|-b-e":0.999}
			self.CPTs["J"]={"+j|+a":0.90, "-j|+a":0.10, 
					"+j|-a":0.05, "-j|-a":0.95}
			self.CPTs["M"]={"+m|+a":0.70, "-m|+a":0.30, 
					"+m|-a":0.01, "-m|-a":0.99}
			self.CPTs["order"]=["B", "E", "A", "J", "M"]
			self.CPTs["parents"]={"B":None, "E":None, "A":"B,E", "J":"A", "M":"A"}

		elif netID == "sprinkler":
			self.CPTs["C"]={"+c":0.50, "-c":0.50}
			self.CPTs["S"]={"+s|+c":0.10, "-s|+c":0.90, 
					"+s|-c":0.50, "-s|-c":0.50}
			self.CPTs["R"]={"+r|+c":0.80, "-r|+c":0.20, 
					"+r|-c":0.20, "-r|-c":0.80}
			self.CPTs["W"]={"+w|+s+r":0.99, "-w|+s+r":0.01, 
					"+w|+s-r":0.90, "-w|+s-r":0.10,
					"+w|-s+r":0.90, "-w|-s+r":0.10,
					"+w|-s-r":0.00, "-w|-s-r":1.00}
			self.CPTs["order"]=["C", "S", "R", "W"]
			self.CPTs["parents"]={"C":None, "S":"C", "R":"C", "W":"S,R"}

		else:
			print("UNKNOWN network="+str(netID))
			exit(0)

	def sampleVariable(self, CPT, conditional):
		sampledValue=None
		randnumber=random.random()

		value1=CPT["+"+conditional]
		value2=CPT["-"+conditional]

		if randnumber<=value1:
			sampledValue="+"+conditional
		else:
			sampledValue="-"+conditional

		return sampledValue.split("|")[0]

	def sampleVariables(self, printEvent):
		event=[]
		sampledVars={}

		for variable in self.CPTs["order"]:
			evidence=""
			conditional=""
			parents=self.CPTs["parents"][variable]
			if parents==None:
				conditional=variable.lower()
			else:
				for parent in parents.split(","):
					evidence+=sampledVars[parent]
				conditional=variable.lower()+"|"+evidence

			sampledValue=self.sampleVariable(self.CPTs[variable], conditional)
			event.append(sampledValue)
			sampledVars[variable]=sampledValue
				
		if printEvent: print(event)
		return event

	def weightedSample(self, query_event):
		random_event = self.sampleVariables(False)
		weight = 1

		# convert sample into true or false format:
		for j in range(0, len(random_event)):
			random_event[j] = random_event[j][:-1]
			if random_event[j] == '+':
				random_event[j] = True
			else:
				random_event[j] = False

		for i in range(0, len(query_event)):

			# Variable that is randomly sampled and does not effec tthe weighting:
			if query_event[i] == "N/A":
				pass

			# If this variable is the unknown variable: 
			if query_event[i] == "find":
				pass

			# Fixed Variable:
			if query_event[i] == True or query_event[i] == False:  # i.e. its an evidence variable. so calculate the weight:
				random_event[i] = query_event[i]	# fix the random event so that it fits the query variable format

				# Now calculate the weight for the "fixed variable" value:
				variable_name = self.CPTs["order"][i]
				parents_name = self.CPTs["parents"][variable_name]

				if parents_name == None:
					if query_event[i] == True:
						weight = weight * self.CPTs[variable_name]["+"+variable_name.lower()]
					else:
						weight = weight * self.CPTs[variable_name]["-"+variable_name.lower()]

				else:
					# Creating a lookup for the dictionary, starting with the unknown variable:
					if query_event[i] == True:
						lookup = '+' + variable_name.lower() + '|'
					else:
						lookup = '-' + variable_name.lower() + '|'

					# for each parent find the random t/f value associated with this event:
					for parent in parents_name.split(","):
						index_of_parent = self.CPTs["order"].index(parent)
						if random_event[index_of_parent] == True:
							lookup = lookup + '+' + parent.lower()
						else:
							lookup = lookup + '-' + parent.lower()

					weight = weight *float(self.CPTs[variable_name][lookup])

		return random_event, weight


	def likelihoodWeighting(self, number_of_samples, query_event):
		count_possible_event_list = []
		prob_true = 0
		prob_false = 0
		w_false = 0
		w_true = 0
		index_to_find = query_event.index("find")

		for i in range(0, number_of_samples):
			sample, weight = self.weightedSample(query_event)
			print(weight, sample)
			if sample[2] == True:
				w_true += weight
			else:
				w_false += weight

		normalised_probability = [(float(w_true) / (float(w_true) + float(w_false))), (float(w_false) / (float(w_true) + float(w_false)))]
		return	normalised_probability


if __name__ == "__main__":
	ps=PriorSampling("sprinkler")
	normalised_probability = ps.likelihoodWeighting(number_of_samples = 5, query_event = [True, "N/A", "find", True]) #  P(rain|sprinkler = true) use "N/A" and "find" = query variabel and true/false  
	print(normalised_probability)