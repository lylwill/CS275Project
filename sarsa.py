from RL import RL

class sarsa(RL):
	def __init__(self, actions, epsilon, alpha=0.3, gamma=1.0):
		RL.__init__(self, actions, epsilon, alpha, gamma)

	def learn(self, state1, action1, reward, state2, action2):
		try:
			qnext = self.getQ(state2, action2)
			# print "qval:", qnext
			self.updateQ(state1, action1, reward, reward+self.gamma*qnext)
		except:
			print "Failed to learn"
