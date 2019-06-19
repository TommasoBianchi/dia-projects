from experiment.subcampaign_algo import Subcampaign_algo
from experiment.context_generation import disaggregate_context

from knapsack.knapsack import Knapsack

from utilities.rounding import round_to_nearest_feasible_superarm
from utilities.print_functions import prettify_super_arm

class Experiment:
    def __init__(self, environment, budget_discretization_steps, daily_budget):
        self.environment = environment
        self.budget_discretization_steps = budget_discretization_steps
        self.daily_budget = daily_budget

    def perform(self, timesteps, context_generation_rate = -1):
        rewards = []

        environment = self.environment.copy()
        num_subcampaigns = len(environment.subcampaigns)

        subcampaign_algos = [Subcampaign_algo(self.budget_discretization_steps.copy()) for _ in range(num_subcampaigns)]
        for i in range(num_subcampaigns):
            samples = [[k * self.daily_budget / 50 for k in range(51)],
                       [sum(environment.get_subcampaign(i).sample(k * self.daily_budget /50, save_sample = False)) for k in range(51)]]
            subcampaign_algos[i].learn_gp_kernel_hyperparameters(samples)

        # Run only when without context generation
        if context_generation_rate < 0:
            regression_errors_max = [[] for _ in range(num_subcampaigns)]
            regression_errors_sum = [[] for _ in range(num_subcampaigns)]

        for t in range(timesteps):

            # Sample from the subcampaign_algos to get clicks estimations
            estimations = []
            for subcampaign_algo in subcampaign_algos:
                estimate = [subcampaign_algo.sample_from_gp(arm) for arm in self.budget_discretization_steps]
                if(sum(estimate) == 0):
                    estimate = [i * 1e-3 for i in range(len(self.budget_discretization_steps))]
                estimate[0] = 0
                estimations.append(estimate)

            # Run knapsack optimization
            super_arm = Knapsack(self.daily_budget, estimations).optimize()

            # Fix for first day
            if t == 0:
                super_arm = [(i, self.daily_budget / num_subcampaigns) for i in range(num_subcampaigns)]
                super_arm = round_to_nearest_feasible_superarm(super_arm, self.budget_discretization_steps)

            # Collect rewards and update subcampaign_algos
            total_reward = 0
            for (subcampaign_id, budget_assigned) in super_arm:
                reward = environment.get_subcampaign(subcampaign_id).sample(budget_assigned)
                total_reward += sum(reward)

                # Fit multiple point to the GPs (one per each class of user inside this subcampaing)
                subcampaign_algos[subcampaign_id].update(budget_assigned, reward)

            print("-------------------------")
            print("t = " + str(t+1) + ", superarm = " + prettify_super_arm(environment, super_arm) + ", reward = " + str(total_reward))

            rewards.append(total_reward)

            # Run only when without context generation
            if context_generation_rate < 0:
                for i in range(num_subcampaigns):
                    regression_rewards = [(x, environment.subcampaigns[i].get_real(x)) for x in self.budget_discretization_steps]
                    regression_errors_max[i].append(
                        subcampaign_algos[i].get_regression_error(points_to_evaluate = regression_rewards))
                    regression_errors_sum[i].append(
                        subcampaign_algos[i].get_regression_error(use_sum = True, points_to_evaluate = regression_rewards))

            # Context generation
            if context_generation_rate > 0 and t < timesteps-1 and (t+1) % context_generation_rate == 0:

                print("--------------------------")
                print("t = " + str(t+1) + ", performing context generation")

                # Disaggreagate contexts
                disaggregate_context(environment, self.budget_discretization_steps, self.daily_budget)

                # Update parameters
                num_subcampaigns = len(environment.subcampaigns)
                subcampaign_algos = [Subcampaign_algo(self.budget_discretization_steps.copy()) for _ in range(num_subcampaigns)]
                for i in range(num_subcampaigns):
                    samples = [[k * self.daily_budget / 50 for k in range(51)],
                               [sum(environment.get_subcampaign(i).sample(k * self.daily_budget / 50, save_sample = False)) for k in range(51)]]
                    subcampaign_algos[i].learn_gp_kernel_hyperparameters(samples)
                
                # Retrain gaussian processes
                for subcampaign_id in range(num_subcampaigns):
                    subcampaign_algo = subcampaign_algos[subcampaign_id]
                    for (arm, sample) in environment.get_subcampaign(subcampaign_id).get_samples():
                        for y in sample:
                           subcampaign_algo.gaussian_process.update_observations_raw(arm, y * len(sample))
                        #subcampaign_algo.gaussian_process.update_observations_raw(arm, sum(sample))
                    subcampaign_algo.gaussian_process.update_model()

        print("-------------------------")

        if context_generation_rate > 0:
            return (rewards, environment, subcampaign_algos)
        else:
            return (rewards, environment, subcampaign_algos, regression_errors_max, regression_errors_sum)