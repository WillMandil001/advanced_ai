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


	def rejectionSampling(self, number_of_samples, event):
		count_possible_event_list = []
		prob_true = 0
		prob_false = 0
		index_to_find = event.index("find")

		for i in range(0, number_of_samples):
			sample = self.sampleVariables(False)
			
			# convert sample into true or false format:
			for j in range(0, len(sample)):
				sample[j] = sample[j][:-1]
				if sample[j] == '+':
					sample[j] = True
				else:
					sample[j] = False

			# rejection:
			for j in range(0, len(event)):
				if event[j] == 'N/A':
					pass
				elif event[j] == 'find':
					pass
				elif event[j] != sample[j]:
					sample = "rejected"
			count_possible_event_list.append(sample)

		count_possible_event_list[:] = (value for value in count_possible_event_list if value != 'rejected')		
		print(count_possible_event_list)

		for j in range(0, len(count_possible_event_list)):
			if count_possible_event_list[j][index_to_find] == True:
				prob_true +=1
			else:
				prob_false +=1

		probability_estimate = [prob_true, prob_false]
		print(probability_estimate)
		probability_estimate_normalised = [(float(prob_true) / (float(prob_true) + float(prob_false))), (float(prob_false) / (float(prob_true) + float(prob_false)))]
		print("Normalised probability estimate = ", probability_estimate_normalised)


if __name__ == "__main__":
	ps=PriorSampling("sprinkler")
	ps.rejectionSampling(number_of_samples=100000, event = [True, True, "find", "N/A"]) #  P(rain|sprinkler = true) use "N/A" and "find" = query variabel and true/false
