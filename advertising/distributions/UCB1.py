try:
    # IMPORT FOR PYCHARM USERS
    from matching.distributions.probability_distribution import Probability_Distribution
except (SystemError, ImportError):
    # IMPORT FOR NON-PYCHARM USERS
    from distributions.probability_distribution import Probability_Distribution

import numpy as np

class UCB1(Probability_Distribution):
    def __init__(self):
        self.empirical_mean = 0
        self.realization_number = 0
        self.current_time = 0

    def sample(self):
        if self.realization_number < 1:
            return 1e100 # Practically equivalent to infinity, to ensure every arm is pulled at least once

        return self.empirical_mean + np.sqrt((2 * np.log(self.current_time)) / self.realization_number)

    def update_parameters(self, new_realization):
        self.empirical_mean = (self.empirical_mean * self.realization_number + new_realization) \
                              / (self.realization_number + 1)

        self.realization_number += 1
