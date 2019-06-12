from knapsack.knapsack import Knapsack

import numpy as np

def disaggregate_context(environment, arms, budget, max_aggregation_factor):
	all_disaggregations = environment.get_combinations()

	augmented_arms = []
	for i in range(1, len(arms)):
		delta = (arms[i] - arms[i - 1]) / max_aggregation_factor
		augmented_arms += [round(arms[i - 1] + delta * x, 3) for x in range(max_aggregation_factor)]
	augmented_arms.append(arms[-1])
	arms = augmented_arms

	optimal_disaggregation = None
	optimal_disaggregation_expected_value = -np.inf

	first = -1

	for disaggregation in all_disaggregations:
		# Generate lower bounds
		lower_bounds = []
		for subcampaign in disaggregation:
			subcampaign_lower_bounds = []
			subcampaign_samples = subcampaign.get_samples()
			for arm in arms:
				arm_rewards = []
				for (pulled_arm, reward) in subcampaign_samples:
					if abs(arm - pulled_arm) < 0.1: # equals avoiding rounding errors
						arm_rewards.append(reward)
				
				# Build gaussian lower bound
				if len(arm_rewards) > 0:
					arm_mean = np.mean(arm_rewards)
					arm_std = np.std(arm_rewards)
					arm_lower_bound = arm_mean - 1.96 * (arm_std / np.sqrt(len(arm_rewards)))
				else:
					arm_lower_bound = -np.inf
				subcampaign_lower_bounds.append(arm_lower_bound)
			lower_bounds.append(subcampaign_lower_bounds)

		# Find optimal arm (Knapsack)
		optimal_super_arm = Knapsack(budget, lower_bounds, arms = arms).optimize()
		optimal_super_arm_value = sum([lower_bounds[i][arms.index(arm)] for (i, arm) in optimal_super_arm])

		# Update optimal disaggregation
		if optimal_super_arm_value > optimal_disaggregation_expected_value:
			optimal_disaggregation_expected_value = optimal_super_arm_value
			optimal_disaggregation = disaggregation

		## TEST
		if first == -1:
			first = optimal_super_arm_value

	print(all_disaggregations[0])
	print(first)
	print(optimal_disaggregation_expected_value)

	environment.subcampaigns = optimal_disaggregation