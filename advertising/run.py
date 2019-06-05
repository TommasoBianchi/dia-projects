from experiment.subcampaign_algo import Subcampaign_algo

from knapsack.knapsack import Knapsack

from utilities.environment_building import build_environment
from utilities.plot_function import plot_function

from config.test_config import get_configuration as get_test_configuration

import matplotlib.pyplot as plt
import numpy as np

############################################
## Configurations
############################################

timesteps = 100
daily_budget = 100
budget_discretization_density = 10
budget_discretization_steps = [i * daily_budget / budget_discretization_density for i in range(budget_discretization_density + 1)]
plot_path = "plots/"

############################################
## Build the environment
############################################

environment = build_environment(get_test_configuration())
num_subcampaigns = len(environment.subcampaigns)

############################################
## Plot environment data
############################################

legend = []
for i in range(num_subcampaigns):
    plot_function(environment.subcampaigns[i].get_real, range(daily_budget))
    plot_function(environment.subcampaigns[i].sample, range(daily_budget))
    legend.append("Subcampaign " + str(i+1) + " real click function")
    legend.append("Subcampaign " + str(i+1) + " noisy click function")

plt.legend(legend, bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Environment")
plt.savefig(plot_path + 'environment.png', bbox_inches='tight', dpi = 300)
plt.close()

############################################
## Build the subcampaign algos
############################################

subcampaign_algos = [Subcampaign_algo(budget_discretization_steps.copy()) for _ in range(num_subcampaigns)]

############################################
## Build the clairvoyant solution
############################################

real_values = []
for subcampaign in environment.subcampaigns:
    real_values.append([subcampaign.get_real(arm) for arm in budget_discretization_steps])
optimal_super_arm = Knapsack(daily_budget, real_values).optimize()
print("Optimal superarm is " + str(optimal_super_arm))
optimal_super_arm_value = sum([environment.subcampaigns[i].get_real(arm) for (i, arm) in optimal_super_arm])
print("Value of optimal superarm = " + str(optimal_super_arm_value))

############################################
## Main loop
############################################

rewards = []
clairvoyant_rewards = []

for t in range(timesteps):

    # Sample from the subcampaign_algos to get clicks estimations
    estimations = []
    for subcampaign_algo in subcampaign_algos:
        estimate = [subcampaign_algo.sample_from_gp(arm) for arm in budget_discretization_steps]
        if(sum(estimate) == 0):
            estimate = [i * 1e-3 for i in range(len(budget_discretization_steps))]
        estimate[0] = 0
        estimations.append(estimate)

    # Run knapsack optimization
    super_arm = Knapsack(daily_budget, estimations).optimize()
    
    # Fix for first day
    if t == 0:
        super_arm = [(i, daily_budget / num_subcampaigns) for i in range(num_subcampaigns)]

    # Collect rewards and update subcampaign_algos
    total_reward = 0
    for (subcampaign_id, budget_assigned) in super_arm:
        reward = environment.get_subcampaign(subcampaign_id).sample(budget_assigned)
        total_reward += reward
        subcampaign_algos[subcampaign_id].update(budget_assigned, reward)

    # Collect clairvoyant rewards
    total_clairvoyant_reward = 0
    for (subcampaign_id, budget_assigned) in optimal_super_arm:
        reward = environment.get_subcampaign(subcampaign_id).sample(budget_assigned)
        total_clairvoyant_reward += reward
    
    print("-------------------------")
    #print(estimations)
    print("t = " + str(t+1) + ", superarm = " + str(super_arm) + ", reward = " + str(total_reward))
    print("-------------------------")

    rewards.append(total_reward)
    clairvoyant_rewards.append(total_clairvoyant_reward)

############################################
## Plot results
############################################

plt.plot(np.cumsum(rewards))
plt.plot(np.cumsum(clairvoyant_rewards))
plt.legend(['GPTS', 'Clairvoyant'], bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Cumulative reward")
plt.savefig(plot_path + 'cumulative_reward.png', bbox_inches='tight', dpi = 300)
plt.close()

plt.plot([(clairvoyant_rewards[i] - rewards[i]) / (i+1) for i in range(len(rewards))])
plt.legend(['GPTS'], bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Average regret")
plt.savefig(plot_path + 'average_regret.png', bbox_inches='tight', dpi = 300)
plt.close()

for i in range(num_subcampaigns):
    plot_function(environment.subcampaigns[i].get_real, range(daily_budget))
    plt.plot(range(daily_budget), [subcampaign_algos[i].gaussian_process.gaussian_process.predict(np.atleast_2d(x).T) for x in range(daily_budget)])
    plt.legend(['Real click function', 'Estimated click function'], bbox_to_anchor = (1.05, 1), loc = 2)
    plt.title("Subcampaign " + str(i+1))
    plt.savefig(plot_path + 'subcampaign_estimation_' + str(i+1) + '.png', bbox_inches='tight', dpi = 300)
    plt.close()