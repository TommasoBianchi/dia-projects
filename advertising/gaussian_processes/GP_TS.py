from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import numpy as np


class GP_TS:
    def __init__(self, n_arms, arms):
        kernel = C(1.0, (1e-3, 1e3))* RBF(1.0, (1e-3, 1e3))
        alpha = 10.0
        self.n_arms = n_arms
        self.means = np.zeros(self.n_arms)
        self.sigmas = np.ones(self.n_arms) *10
        self.arms = arms
        self.collected_rewards = np.array([])
        self.pulled_arms = []
        self.gaussian_process = GaussianProcessRegressor(kernel=kernel, alpha=alpha**2, normalize_y=True,
                                                         n_restarts_optimizer=9)

    def update_model(self):
        x = np.atleast_2d(self.pulled_arms).T
        y = self.collected_rewards
        self.gaussian_process.fit(x, y)
        self.means, self.sigmas = self.gaussian_process.predict(np.atleast_2d(self.arms).T, return_std=True)
        self.sigmas = np.maximum(self.sigmas, 1e-2)

    def update_observations(self, arm_idx, reward):
        self.pulled_arms.append(self.arms[arm_idx])
        self.collected_rewards = np.append(self.collected_rewards, reward)

    def sample(self, arm_idx):
        x = self.arms[arm_idx]
        return self.gaussian_process.predict(np.atleast_2d(x).T)[0]

    def find_arm(self, arm):
        for idx in range(self.n_arms):
            if self.arms[idx] == arm:
                return idx
        return False
