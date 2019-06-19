from experiment.experiment import Experiment

from knapsack.knapsack import Knapsack

from utilities.environment_building import build_environment
from utilities.plot_function import plot_function
from utilities.print_functions import prettify_super_arm

from config.test_config import get_configuration as get_test_configuration

import matplotlib.pyplot as plt
import numpy as np

############################################
## Configurations
############################################

timesteps_stationary = 50
timesteps_context_generation = 0
context_generation_rate = 10
daily_budget = 100
budget_discretization_density = 20
budget_discretization_steps = [i * daily_budget / budget_discretization_density for i in range(budget_discretization_density + 1)]

plot_path = "plots/"
#plot_path = "advertising/plots/"

############################################
## Build the original_environment
############################################

original_environment = build_environment(get_test_configuration())

num_subcampaigns = len(original_environment.subcampaigns)

############################################
## Plot original_environment data
############################################

legend = []
for subcampaign in original_environment.subcampaigns:
    subcampaign_name = str(subcampaign.get_classes_ids())
    plot_function(subcampaign.get_real, range(daily_budget))
    plot_function(lambda x: sum(subcampaign.sample(x, save_sample = False)), range(daily_budget))
    legend.append("Subcampaign " + subcampaign_name + " real click function")
    legend.append("Subcampaign " + subcampaign_name + " noisy click function")

plt.legend(legend, bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Environment - Aggregated")
plt.savefig(plot_path + 'environment_aggregated.png', bbox_inches='tight', dpi = 300)
plt.close()

legend = []
for subcampaign in original_environment.subcampaigns:
    for click_function in subcampaign.classes:
        subcampaign_name = str((click_function.id))
        plot_function(click_function.real_function_value, range(daily_budget))
        plot_function(lambda x: click_function.sample(x, save_sample = False), range(daily_budget))
        legend.append("Subcampaign " + subcampaign_name + " real click function")
        legend.append("Subcampaign " + subcampaign_name + " noisy click function")

plt.legend(legend, bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Environment - Disaggreagated")
plt.savefig(plot_path + 'environment_disaggregated.png', bbox_inches='tight', dpi = 300)
plt.close()

############################################
## Build the clairvoyant solution
############################################

# With aggregated subcampaigns
real_values = []
for subcampaign in original_environment.subcampaigns:
    real_values.append([subcampaign.get_real(arm) for arm in budget_discretization_steps])
optimal_super_arm = Knapsack(daily_budget, real_values).optimize()
print("Optimal superarm is " + prettify_super_arm(original_environment, optimal_super_arm))
optimal_super_arm_value = sum([original_environment.subcampaigns[i].get_real(arm) for (i, arm) in optimal_super_arm])
print("Value of optimal superarm = " + str(optimal_super_arm_value))

# With fully disaggregated subcampaigns
real_values = []
subclasses_dict = dict()
subclass_index = 0
for subcampaign in original_environment.subcampaigns:
    for subclass in subcampaign.classes:
        real_values.append([subclass.real_function_value(arm) for arm in budget_discretization_steps])
        subclasses_dict[subclass_index] = subclass
        subclass_index += 1
optimal_disaggregated_super_arm = Knapsack(daily_budget, real_values).optimize()
print("Optimal disaggregated superarm is " + str([(subclasses_dict[i].id, arm) for (i, arm) in optimal_disaggregated_super_arm]))
optimal_disaggregated_super_arm_value = sum([subclasses_dict[i].real_function_value(arm) for (i, arm) in optimal_disaggregated_super_arm])
print("Value of optimal disaggregated superarm = " + str(optimal_disaggregated_super_arm_value))

clairvoyant_rewards = [optimal_super_arm_value for _ in range(timesteps_stationary)]
disaggregated_clairvoyant_rewards = [optimal_disaggregated_super_arm_value for _ in range(timesteps_context_generation)]

############################################
## Define GPTS prior
############################################

GPTS_prior = lambda x: 3 * x

############################################
## Perform experiments
############################################

experiment = Experiment(original_environment, budget_discretization_steps, daily_budget, GPTS_prior)

print("------ GPTS stationary ------")
(stationary_rewards, stationary_final_environment, stationary_final_subcampaign_algos,
 regression_errors_max, regression_errors_sum) = experiment.perform(timesteps_stationary)

print("------ GPTS context generation ------")
(context_generation_rewards, context_generation_final_environment,
 context_generation_final_subcampaign_algos) = experiment.perform(timesteps_context_generation, context_generation_rate)

############################################
## Plot results
############################################

cumulative_stationary_reward = np.cumsum(stationary_rewards)
cumulative_context_generation_reward = np.cumsum(context_generation_rewards)
cumulative_clairvoyant_reward = np.cumsum(clairvoyant_rewards)
cumulative_disaggregated_clairvoyant_reward = np.cumsum(disaggregated_clairvoyant_rewards)

# Cumulative rewards

plt.plot(cumulative_stationary_reward)
plt.plot(cumulative_context_generation_reward)
plt.plot(cumulative_clairvoyant_reward)
plt.plot(cumulative_disaggregated_clairvoyant_reward)
plt.legend(['GPTS - Stationary', 'GPTS - Context generation', 'Clairvoyant', 'Clairvoyant - Optimal context'], bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Cumulative reward")
plt.savefig(plot_path + 'cumulative_reward.png', bbox_inches='tight', dpi = 300)
plt.close()

# Average regrets

plt.plot([(cumulative_clairvoyant_reward[i] - cumulative_stationary_reward[i]) / (i+1) for i in range(len(cumulative_stationary_reward))])
plt.plot([(cumulative_disaggregated_clairvoyant_reward[i] - cumulative_context_generation_reward[i]) / (i+1) for i in range(len(cumulative_context_generation_reward))])
plt.legend(['GPTS - Stationary', 'GPTS - Context generation'], bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Average regret")
plt.savefig(plot_path + 'average_regret.png', bbox_inches='tight', dpi = 300)
plt.close()

# Average percentage regrets

plt.plot([((cumulative_clairvoyant_reward[i] - cumulative_stationary_reward[i]) / (i+1)) / optimal_super_arm_value 
                for i in range(len(cumulative_stationary_reward))])
plt.plot([((cumulative_disaggregated_clairvoyant_reward[i] - cumulative_context_generation_reward[i]) / (i+1)) / optimal_disaggregated_super_arm_value
                for i in range(len(cumulative_context_generation_reward))])
plt.legend(['GPTS - Stationary', 'GPTS - Context generation'], bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Average percentage regret")
plt.savefig(plot_path + 'average_percentage_regret.png', bbox_inches='tight', dpi = 300)
plt.close()

# GP estimations and number of pulls per arm - stationary

for i in range(len(stationary_final_environment.subcampaigns)):
    subcampaign = stationary_final_environment.subcampaigns[i]
    subcampaign_name = str(subcampaign.get_classes_ids())
    plot_function(subcampaign.get_real, range(daily_budget))
    
    gp = stationary_final_subcampaign_algos[i].gaussian_process.gaussian_process
    mean_function = lambda x: gp.predict(np.atleast_2d(x).T)[0] + GPTS_prior(x)
    std_function = lambda x: gp.predict(np.atleast_2d(x).T, return_std = True)[1][0]
    plot_function(mean_function, range(daily_budget), std_function)
    
    plt.legend(['Real click function', 'Estimated click function'], bbox_to_anchor = (1.05, 1), loc = 2)
    plt.title("Subcampaign " + subcampaign_name)
    plt.savefig(plot_path + 'stationary_subcampaign_estimation_' + subcampaign_name + '.png', bbox_inches='tight', dpi = 300)
    plt.close()

    plot_function(lambda x: stationary_final_subcampaign_algos[i].get_pulled_arms_amount(x) if (x in budget_discretization_steps) else 0, range(daily_budget))
    plt.title("Subcampaign " + subcampaign_name + " number of pulled arms")
    plt.savefig(plot_path + 'stationary_pulled_arms_subcampaign_' + subcampaign_name + '.png', bbox_inches='tight', dpi = 300)
    plt.close()

# GP estimations and number of pulls per arm - context_generation

for i in range(len(context_generation_final_environment.subcampaigns)):
    subcampaign = context_generation_final_environment.subcampaigns[i]
    subcampaign_name = str(subcampaign.get_classes_ids())
    plot_function(subcampaign.get_real, range(daily_budget))
    
    gp = context_generation_final_subcampaign_algos[i].gaussian_process.gaussian_process
    
    mean_function = lambda x: gp.predict(np.atleast_2d(x).T)[0] + GPTS_prior(x)
    std_function = lambda x: gp.predict(np.atleast_2d(x).T, return_std = True)[1][0]
    plot_function(mean_function, range(daily_budget), std_function)
    
    plt.legend(['Real click function', 'Estimated click function'], bbox_to_anchor = (1.05, 1), loc = 2)
    plt.title("Subcampaign " + subcampaign_name)
    plt.savefig(plot_path + 'context_generation_subcampaign_estimation_' + subcampaign_name + '.png', bbox_inches='tight', dpi = 300)
    plt.close()

    plot_function(lambda x: context_generation_final_subcampaign_algos[i].get_pulled_arms_amount(x) if (x in budget_discretization_steps) else 0, range(daily_budget))
    plt.title("Subcampaign " + subcampaign_name + " number of pulled arms")
    plt.savefig(plot_path + 'context_generation_pulled_arms_subcampaign_' + subcampaign_name + '.png', bbox_inches='tight', dpi = 300)
    plt.close()

# Subcampaign regression errors (run only for the stationary case)

legend = []
for i in range(len(stationary_final_environment.subcampaigns)):
    plt.plot(regression_errors_max[i])
    subcampaign_name = str(context_generation_final_environment.subcampaigns[i].get_classes_ids())
    legend.append("Subcampaign " + subcampaign_name)
plt.legend(legend, bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Subcampaign regression error (Max)")
plt.savefig(plot_path + 'regression_errors_max.png', bbox_inches='tight', dpi = 300)
plt.close()

legend = []
for i in range(len(stationary_final_environment.subcampaigns)):
    plt.plot(regression_errors_sum[i])
    subcampaign_name = str(context_generation_final_environment.subcampaigns[i].get_classes_ids())
    legend.append("Subcampaign " + subcampaign_name)
plt.legend(legend, bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Subcampaign regression error (Sum)")
plt.savefig(plot_path + 'regression_errors_sum.png', bbox_inches='tight', dpi = 300)
plt.close()