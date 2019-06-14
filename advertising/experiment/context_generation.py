from experiment.subcampaign_algo import Subcampaign_algo

from knapsack.knapsack import Knapsack

import numpy as np

def disaggregate_context(environment, arms, budget):
    all_disaggregations = environment.get_combinations()

    optimal_disaggregation = None
    optimal_disaggregation_expected_value = -np.inf

    for disaggregation in all_disaggregations:
        # Train a set of GPs on this level of disaggregation
        subcampaign_algos = [Subcampaign_algo(arms.copy()) for _ in range(len(disaggregation))]
        for subcampaign_id in range(len(disaggregation)):
            subcampaign = disaggregation[subcampaign_id]
            subcampaign_algo = subcampaign_algos[subcampaign_id]
            for t in range(len(subcampaign.classes[0].samples)):
                iteration_samples = [c.samples[t] for c in subcampaign.classes]
                (arm, sample) = (sum([x[0] for x in iteration_samples]), tuple(map(lambda s: s[1], iteration_samples)))
                for y in sample:
                    subcampaign_algo.gaussian_process.update_observations_raw(arm, y * len(sample))
                #subcampaign_algo.gaussian_process.update_observations_raw(arm, sum(sample))
            subcampaign_algo.gaussian_process.update_model()

        # Generate lower bounds from the GPs
        lower_bounds = []
        for subcampaign_algo in subcampaign_algos:
            subcampaign_lower_bounds = [subcampaign_algo.lower_bound_from_gp(arm) for arm in arms]
            lower_bounds.append(subcampaign_lower_bounds)

        # Find optimal arm (Knapsack)
        optimal_super_arm = Knapsack(budget, lower_bounds, arms = arms).optimize()
        optimal_super_arm_value = sum([lower_bounds[i][arms.index(arm)] for (i, arm) in optimal_super_arm])

        # Update optimal disaggregation
        if optimal_super_arm_value > optimal_disaggregation_expected_value:
            optimal_disaggregation_expected_value = optimal_super_arm_value
            optimal_disaggregation = disaggregation

    environment.subcampaigns = optimal_disaggregation