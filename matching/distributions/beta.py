# IMPORT PYCHARM USERS
from matching.distributions.probability_distribution import Probability_Distribution

# IMPORT NON-PYCHARM USERS
# from distributions.probability_distribution import Probability_Distribution
import numpy as np


class Beta(Probability_Distribution):
    def __init__(self):
        self.alpha = 1
        self.beta = 1

    def sample(self, parameters):
        return np.random.beta(self.alpha, self.beta)

    def update_parameters(self, parameters):
        self.alpha = parameters[0]
        self.beta = parameters[1]
