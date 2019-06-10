from gaussian_processes import GP_TS

class Subcampaign_algo:
    def __init__(self, arms):
        self.gaussian_process = GP_TS.GP_TS(arms)
        self.arms = arms

    # Add the new observation to the model and update the model
    def update(self, arm, reward):
        arm_idx = self.gaussian_process.find_arm(arm)
        self.gaussian_process.update_observations(arm_idx, reward)
        self.gaussian_process.update_model()

    # Get the prediction of the GP for a given arm
    def sample_from_gp(self, arm):
        arm_idx = self.gaussian_process.find_arm(arm)
        return self.gaussian_process.sample(arm_idx)

    # Get the variance of the GP for a given arm
    def get_sigma(self, arm):
        arm_idx = self.gaussian_process.find_arm(arm)
        return self.gaussian_process.get_sigma(arm_idx)

    # Get the regression error as the maximum of the regression errros over each arm
    def get_regression_error(self, use_sum = False):
        if use_sum:
            #return sum([self.gaussian_process.get_arm_average_regression_error(arm) for arm in self.arms])
            return self.gaussian_process.get_average_regression_error()
        else:   
            return max([self.gaussian_process.get_arm_average_regression_error(arm) for arm in self.arms])

    def get_pulled_arms_amount(self, arm):
        return len(list(filter(lambda x: x == arm, self.gaussian_process.pulled_arms)))