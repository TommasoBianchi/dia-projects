try:
	# IMPORT FOR PYCHARM USERS
	from matching.distributions.probability_distribution import Probability_Distribution
except (SystemError, ImportError):
	# IMPORT FOR NON-PYCHARM USERS
	from distributions.probability_distribution import Probability_Distribution
	
import random

class Uniform_Discrete(Probability_Distribution):
	def __init__(self, min, max):
		self.min = min
		self.max = max

	def sample(self):
		return random.randint(self.min, self.max)

	def update_parameters(self, parameters):
		self.min = parameters[0]
		self.max = parameters[1]