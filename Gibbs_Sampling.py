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

	def gibbsSampling(self, number_of_samples, query_event):
		current_state = []
		markov_blanket_list = []
		# GENERATE INITIAL STATE:
		for i in range(0, len(query_event)):
			if query_event[i] == True or query_event[i] == False:
				current_state.append(query_event[i])
			else:
				randnumber=random.random()
				if randnumber > 0.5:
					current_state.append(True)
				else:
					current_state.append(False)

		# FIND ALL RELEVANT MARKOV BLANKETS.
		for i in range(0, len(current_state)):
			# if its a nonevidence variable:
			if query_event[i] != True and query_event[i] != False:

				# Calculate the markov blanket and produce a probability lookup:
				# 1. find the parents:
				current_variable = self.CPTs["order"][i]
				parents = []
				parents.append(self.CPTs["parents"][current_variable])

				# 2. find the children:
				children = []
				childrens_parents = []
				markov_blanket = []
				for j in range(0, len(query_event)):
					if str(current_variable) in  str(self.CPTs["parents"][self.CPTs["order"][j]]):
						children.append(str(self.CPTs["order"][j]))

				# 3. childs other parents:
				for j in children:
					childs_parents_string = self.CPTs["parents"][j]
					for parent in childs_parents_string.split(","):
						childrens_parents.append(parent)

				# 4. create markov blanket list:
				for item in parents:
					markov_blanket.append(item)
				for item in children:
					markov_blanket.append(item)
				for item in childrens_parents:
					markov_blanket.append(item)

				markov_blanket = list(dict.fromkeys(markov_blanket))  # remove repeated variables
				markov_blanket.remove(current_variable)  # remove the current variable if included
				# remove none values:
				for j in markov_blanket:
					if j == None:
						markov_blanket.remove(j)

				print markov_blanket
				markov_blanket_list.append(markov_blanket)

		# CALCULATE PROBABILITY ESTIMATE:
		print markov_blanket_list
		for i in range(0, number_of_samples):
			# 1. loop through each non_evidence variable in current state and create new state using calculated prob from the markov_blanket of that variable
			for j in range(0, len(current_state)):
				markov_list_index = 0
				if query_event == True or query_event == False:
					pass
				else:
					markov_blanket = markov_blanket_list[markov_list_index]
					# 1. calculate the transition probabilityfor this sample, using true/false values from the current state.

					markov_list_index += 1
					# calculate probability for this variable given the markov blanket:



			# 2. for each new state where the "find" variable == true, add to a counter.
			# 3. then normalse and return probability estimate.


if __name__ == "__main__":
	ps=PriorSampling("sprinkler")
	ps.gibbsSampling(number_of_samples = 100000, query_event = ["N/A", True, "find", True]) #  P(rain|sprinkler = true) use "N/A" and "find" = query variabel and true/false  
