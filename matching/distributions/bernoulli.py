from distributions.probability_distribution import Probability_Distribution
import numpy as np

class Bernoulli(Probability_Distribution):
	def __init__(self, p):
		self.p = p

	def sample(self):
		return np.random.choice([0, 1], p = [1 - self.p, self.p])

	def update_parameters(self, parameters):
		self.p = parameters[0]