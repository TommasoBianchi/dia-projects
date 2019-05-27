from advertising.gaussian_processes import GP_TS

class Subcampaign_algo:
    def __init__(self, num_arms, arms):
        self.gaussian_process = GP_TS.GP_TS(num_arms, arms)

    def update(self, arm, reward):
        arm_idx = self.gaussian_process.find_arm(arm)
        self.gaussian_process.update_observations(arm_idx, reward)
        self.gaussian_process.update_model()

    def sample_from_gp(self, arm):
        arm_idx = self.gaussian_process.find_arm(arm)
        return self.gaussian_process.sample(arm_idx)
