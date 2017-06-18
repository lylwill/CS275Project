import random
class RL:
	QLearn = 1
	SARSA = 2
	def __init__(self, actions, epsilon, alpha, gamma):
		self.q = {}
		self.actions = actions
		self.epsilon = epsilon
		self.alpha = alpha
		self.gamma = gamma

	def choose_action(self, state):
		q = [self.getQ(state, a) for a in self.actions]
		maxQ = max(q)
		try:
			if random.random() < self.epsilon:
				minQ = min(q)
				mag = max(abs(maxQ), abs(minQ))
				q = [q[i] + random.random() * mag - .5*mag for i in range(len(self.actions))]
				maxQ = max(q)
			
			count = q.count(maxQ)
			if count > 1:
				best = [i for i in range(len(self.actions)) if q[i] == maxQ]
				i = random.choice(best)
			else:
				i = q.index(maxQ)
			action = self.actions[i]
			return action
		except:
			print "Failed to choose an action in q learning"

	def getQ(self, state, action):
		return self.q.get((state, action), 0.0)

	def printQ(self):
		keys = self.q.keys()
		states = list(set([a for a,b in keys]))
		actions = list(set([b for a,b in keys]))
		dstates = ["".join([str(int(t)) for t in list(tup)]) for tup in states]
		print (" "*4) + " ".join(["%8s" % ("("+s+")") for s in dstates])
		for a in actions:
			print ("%3d " % (a)) + \
				" ".join(["%8.2f" % (self.getQ(s,a)) for s in states])


	def updateQ(self, state, action, reward, value):
		try:
			oldv = self.q.get((state, action), None)
			if oldv is None:
				self.q[(state, action)] = reward
			else:
				self.q[(state, action)] = oldv + self.alpha * (value - oldv)
		except:
			print "Failed to update q value in q learning"



