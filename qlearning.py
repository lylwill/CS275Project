from RL import RL

class qlearning(RL):
	def __init__(self, actions, epsilon, alpha=0.2, gamma=1.0):
		RL.__init__(self, actions, epsilon, alpha, gamma)

	def learn(self, state1, action, reward, state2):
		try:
			q = [self.getQ(state2, a) for a in self.actions]
			maxQ = max(q)
			self.updateQ(state1, action, reward, reward+self.gamma*maxQ)
			# self.printQ()
		except:
			print "Failed to learn"

