from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import numpy as np


class GP_TS:
    def __init__(self, arms, kernel=C(1.0, (1e-3, 1e3))*RBF(1.0, (1e-3, 1e3)), alpha=10.0):
        self.n_arms = len(arms)
        self.predicted_arms = np.zeros(self.n_arms)
        self.sigmas = np.ones(self.n_arms) * 10
        self.arms = arms
        self.collected_rewards = np.array([])
        self.pulled_arms = []
        self.gaussian_process = GaussianProcessRegressor(kernel=kernel, alpha=alpha**2, normalize_y=True,
                                                         n_restarts_optimizer=9)

    # Fit the gaussian process using the pulled arms and their rewards.
    # It saves the results of the prediction in self.predicted_arms and saves the sigma of each arm in self.sigmas
    def update_model(self):
        x = np.atleast_2d(self.pulled_arms).T
        y = self.collected_rewards
        self.gaussian_process.fit(x, y)
        self.predicted_arms, self.sigmas = self.gaussian_process.predict(np.atleast_2d(self.arms).T, return_std=True)
        self.sigmas = np.maximum(self.sigmas, 1e-2) #sigmas must be positive

    # Add the new observation in the model
    def update_observations(self, arm_idx, reward):
        self.pulled_arms.append(self.arms[arm_idx])
        self.collected_rewards = np.append(self.collected_rewards, reward)

    # Get the prediction of a given arm
    def sample(self, arm_idx):
        return self.predicted_arms[arm_idx]

    # Get the variance of a given arm
    def get_sigma(self, arm_idx):
        return self.sigmas[arm_idx]

    # Find the index of the given arm in self.arm
    def find_arm(self, arm):
        for idx in range(self.n_arms):
            if self.arms[idx] == arm:
                return idx
        return False
