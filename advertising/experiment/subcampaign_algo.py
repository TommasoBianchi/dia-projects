from gaussian_processes import GP_TS

class Subcampaign_algo:
    def __init__(self, arms):
        self.gaussian_process = GP_TS.GP_TS(arms)

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