try:
	# IMPORT PYCHARM USERS
	from matching.distributions.probability_distribution import Probability_Distribution
except (SystemError, ImportError):
	# IMPORT NON-PYCHARM USERS
	from distributions.probability_distribution import Probability_Distribution

import numpy as np


class Beta(Probability_Distribution):
    def __init__(self):
        self.alpha = 1
        self.beta = 1

    def sample(self):
        return np.random.beta(self.alpha, self.beta)

    def update_parameters(self, parameters_delta):
        self.alpha += parameters_delta[0]
        self.beta += parameters_delta[1]