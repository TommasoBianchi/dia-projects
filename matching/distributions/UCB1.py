from matching.distributions.probability_distribution import Probability_Distribution
import numpy as np

class UCB1(Probability_Distribution):
    def __init__(self):
        self.empirical_mean = 0
        self.realization_number = 0

    def sample(self, current_time):
        return self.empirical_mean - np.sqrt((2*np.log(current_time)/(self.realization_number * (current_time - 1))))

    def update_parameters(self, new_realization):
        self.empirical_mean = (self.empirical_mean * self.realization_number + new_realization) \
                              / (self.realization_number + 1)

        self.realization_number += 1
