from distributions.probability_distribution import Probability_Distribution
import numpy as np

class Gaussian(Probability_Distribution):
	def __init__(self, mean, variance):
		self.mean = mean
		self.variance = variance

	def sample(self):
		return np.random.normal(self.mean, self.variance)

	def update_parameters(self, parameters):
		self.mean = parameters[0]
		self.variance = parameters[1]