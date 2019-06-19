from gaussian_processes import GP_TS

class Subcampaign_algo:
    def __init__(self, arms, GPTS_prior = None):
        self.gaussian_process = GP_TS.GP_TS(arms, prior = GPTS_prior)
        self.arms = arms

    # Add the new observation to the model and update the model
    def update(self, arm, reward, update_model = True):
        if type(reward) != type(tuple()):
            reward = (reward,)

        arm_idx = self.gaussian_process.find_arm(arm)

        for y in reward:
            self.gaussian_process.update_observations(arm_idx, y * len(reward))
        if update_model:
            self.gaussian_process.update_model()

    # Get the prediction of the GP for a given arm
    def sample_from_gp(self, arm):
        arm_idx = self.gaussian_process.find_arm(arm)
        return self.gaussian_process.sample(arm_idx)

    # Get the lower bound (95% gaussian) of the GP for a given arm
    def lower_bound_from_gp(self, arm):
        arm_idx = self.gaussian_process.find_arm(arm)
        return self.gaussian_process.lower_bound(arm_idx)

    # Get the variance of the GP for a given arm
    def get_sigma(self, arm):
        arm_idx = self.gaussian_process.find_arm(arm)
        return self.gaussian_process.get_sigma(arm_idx)

    # Get the regression error as the maximum of the regression errros over each arm
    def get_regression_error(self, use_sum = False, points_to_evaluate = None):
        if use_sum:
            #return sum([self.gaussian_process.get_arm_average_regression_error(arm) for arm in self.arms])
            return self.gaussian_process.get_average_regression_error(points_to_evaluate)
        else:   
            return max([self.gaussian_process.get_arm_average_regression_error(arm, points_to_evaluate) for arm in self.arms])

    def get_pulled_arms_amount(self, arm):
        return len(list(filter(lambda x: x == arm, self.gaussian_process.pulled_arms)))

    def learn_gp_kernel_hyperparameters(self, samples):
        self.gaussian_process.learn_kernel_hyperparameters(samples)