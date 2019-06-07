try:
    # IMPORT FOR PYCHARM USERS

    from matching.environment.class_env import Class_Env
    from matching.environment.class_env_edge import Class_Env_Edge
    from matching.environment.environment import Environment
    from matching.environment.restorable_environment import RestorableEnvironment

    from matching.distributions.uniform_discrete import Uniform_Discrete
    from matching.distributions.bernoulli import Bernoulli
    from matching.distributions.gaussian import Gaussian

    from matching.config.random_config import get_configuration as get_random_configuration
    from matching.config.test_config import get_configuration as get_test_configuration
    from matching.config.multiphase_config import get_configuration as get_test_multiphase_configuration

    from matching.experiment.experiment import Experiment, LearnerType, LowerBoundType

except (SystemError, ImportError):
    # IMPORT FOR NON-PYCHARM USERS
    
    from environment.class_env import Class_Env
    from environment.class_env_edge import Class_Env_Edge
    from environment.environment import Environment
    from environment.restorable_environment import RestorableEnvironment

    from distributions import Uniform_Discrete
    from distributions import Bernoulli
    from distributions import Gaussian

    from config.random_config import get_configuration as get_random_configuration
    from config.test_config import get_configuration as get_test_configuration
    from config.test_multiphase_config import get_configuration as get_test_multiphase_configuration

    from experiment import Experiment, LearnerType, LowerBoundType

import matplotlib.pyplot as plt

import time
import numpy as np

###############################################
# Configurations
###############################################

num_days = 500    # Number of days the experiment is run

###############################################
# Build environment (from config file)
###############################################

env_classes = []
phase_lengths = []

configuration = get_test_multiphase_configuration()
for phase_data in configuration['phase_data']:
    phase_lengths.append(phase_data['duration'])
    phase_env_classes = []

    for (id, ldata) in enumerate(phase_data['left_classes']):
        phase_env_classes.append(Class_Env(id, True, 
                                           Gaussian(ldata['new_node_rate_mean'], ldata['new_node_rate_variance']), 
                                           Uniform_Discrete(ldata['time_to_stay_min'], ldata['time_to_stay_max'])))
    num_left_classes = len(phase_data['left_classes'])
    for (id, ldata) in enumerate(phase_data['right_classes']):
        phase_env_classes.append(Class_Env(id + num_left_classes, False, 
                                           Gaussian(ldata['new_node_rate_mean'], ldata['new_node_rate_variance']), 
                                           Uniform_Discrete(ldata['time_to_stay_min'], ldata['time_to_stay_max'])))
    for (ids, edge_data) in phase_data['edge_data'].items():
        class_edge = Class_Env_Edge(Bernoulli(edge_data['mean']), edge_data['weight'])
        l_class = [c for c in phase_env_classes if c.id == ids[0]][0]
        r_class = [c for c in phase_env_classes if c.id == ids[1] + num_left_classes][0]
        l_class.set_edge_data(r_class, class_edge)
        r_class.set_edge_data(l_class, class_edge)

    env_classes.append(phase_env_classes)

environment = RestorableEnvironment(env_classes)

###############################################
# Run experiments
###############################################

experiment = Experiment(environment, phase_lengths, min_phase_length = 3, seed = int(time.time()))

# Clairvoyant (knows context structure and mean of all distributions)
start_time = time.time()
clairvoyant_rewards, clairvoyant_monitor = experiment.perform(num_days, LearnerType.Clairvoyant, debug_info = False)
print("Clairvoyant executed in " + str(time.time() - start_time) + " seconds")

# Thompson sampling (stationary)
start_time = time.time()
ts_rewards, ts_monitor = experiment.perform(num_days, LearnerType.ThompsonSampling, debug_info = False)
print("TS executed in " + str(time.time() - start_time) + " seconds")

# UCB1 (stationary)
start_time = time.time()
ucb1_rewards, ucb1_monitor = experiment.perform(num_days, LearnerType.UCB1, debug_info = False)
print("UCB1 executed in " + str(time.time() - start_time) + " seconds")

# Thompson sampling that perfectly knows the true context structure
start_time = time.time()
ts_known_ctx_rewards, ts_known_ctx_monitor = experiment.perform(num_days, LearnerType.ThompsonSampling, 
                                                                context_structure = phase_lengths, debug_info = False)
print("TS-known-ctx executed in " + str(time.time() - start_time) + " seconds")

# UCB1 that perfectly knows the true context structure
start_time = time.time()
ucb1_known_ctx_rewards, ucb1_known_ctx_monitor = experiment.perform(num_days, LearnerType.UCB1, 
                                                                    context_structure = phase_lengths,  debug_info = False)
print("UCB1-known-ctx executed in " + str(time.time() - start_time) + " seconds")

# Thompson sampling with context generation (hoeffding lower bounds)
start_time = time.time()
ts_ctx_rewards, ts_ctx_monitor = experiment.perform(num_days, LearnerType.ThompsonSampling,
                                    context_generation_every_day = int(num_days / 3) + 1, debug_info = False)
print("TS-context executed in " + str(time.time() - start_time) + " seconds")

# UCB1 with context generation (hoeffding lower bounds)
start_time = time.time()
ucb1_ctx_rewards, ucb1_ctx_monitor = experiment.perform(num_days, LearnerType.UCB1,
                                      context_generation_every_day = int(num_days / 3) + 1, debug_info = False)
print("UCB1-context executed in " + str(time.time() - start_time) + " seconds")

print(ts_ctx_monitor.get_generated_context_structures())
print(ucb1_ctx_monitor.get_generated_context_structures())

# Thompson sampling with context generation (gaussian lower bounds)
start_time = time.time()
ts_ctx_gaussian_rewards, ts_ctx_gaussian_monitor = experiment.perform(num_days, LearnerType.ThompsonSampling, lower_bound_type = LowerBoundType.Gaussian,
                                    context_generation_every_day = int(num_days / 3) + 1, debug_info = False)
print("TS-context-gaussian executed in " + str(time.time() - start_time) + " seconds")

# UCB1 with context generation (gaussian lower bounds)
start_time = time.time()
ucb1_ctx_gaussian_rewards, ucb1_ctx_gaussian_monitor = experiment.perform(num_days, LearnerType.UCB1, lower_bound_type = LowerBoundType.Gaussian,
                                      context_generation_every_day = int(num_days / 3) + 1, debug_info = False)
print("UCB1-context-gaussian executed in " + str(time.time() - start_time) + " seconds")

print(ts_ctx_gaussian_monitor.get_generated_context_structures())
print(ucb1_ctx_gaussian_monitor.get_generated_context_structures())

# Thompson sampling with context generation (hybrid lower bounds)
start_time = time.time()
ts_ctx_hybrid_rewards, ts_ctx_hybrid_monitor = experiment.perform(num_days, LearnerType.ThompsonSampling, lower_bound_type = LowerBoundType.Hybrid,
                                    context_generation_every_day = int(num_days / 3) + 1, debug_info = False)
print("TS-context-hybrid executed in " + str(time.time() - start_time) + " seconds")

# UCB1 with context generation (hybrid lower bounds)
start_time = time.time()
ucb1_ctx_hybrid_rewards, ucb1_ctx_hybrid_monitor = experiment.perform(num_days, LearnerType.UCB1, lower_bound_type = LowerBoundType.Hybrid,
                                      context_generation_every_day = int(num_days / 3) + 1, debug_info = False)
print("UCB1-context-hybrid executed in " + str(time.time() - start_time) + " seconds")

print(ts_ctx_hybrid_monitor.get_generated_context_structures())
print(ucb1_ctx_hybrid_monitor.get_generated_context_structures())

###############################################
# Plotting performances (i.e. rewards/regrets)
###############################################

clairvoyant_cum_rewards = np.cumsum(clairvoyant_rewards).tolist()
ts_cum_rewards = np.cumsum(ts_rewards).tolist()
ucb1_cum_rewards = np.cumsum(ucb1_rewards).tolist()
ts_known_ctx_cum_rewards = np.cumsum(ts_known_ctx_rewards).tolist()
ucb1_known_ctx_cum_rewards = np.cumsum(ucb1_known_ctx_rewards).tolist()
ts_ctx_cum_rewards = np.cumsum(ts_ctx_rewards).tolist()
ucb1_ctx_cum_rewards = np.cumsum(ucb1_ctx_rewards).tolist()
ts_ctx_gaussian_cum_rewards = np.cumsum(ts_ctx_gaussian_rewards).tolist()
ucb1_ctx_gaussian_cum_rewards = np.cumsum(ucb1_ctx_gaussian_rewards).tolist()
ts_ctx_hybrid_cum_rewards = np.cumsum(ts_ctx_hybrid_rewards).tolist()
ucb1_ctx_hybrid_cum_rewards = np.cumsum(ucb1_ctx_hybrid_rewards).tolist()

plot_path = 'plots/'

plt.plot(clairvoyant_cum_rewards)
plt.plot(ts_cum_rewards)
plt.plot(ucb1_cum_rewards)
plt.plot(ts_known_ctx_cum_rewards)
plt.plot(ucb1_known_ctx_cum_rewards)
plt.gca().set_prop_cycle(None)
plt.plot(ts_ctx_cum_rewards, linestyle='--')
plt.plot(ucb1_ctx_cum_rewards, linestyle='--')
plt.plot(ts_ctx_gaussian_cum_rewards, linestyle='--')
plt.plot(ucb1_ctx_gaussian_cum_rewards, linestyle='--')
plt.plot(ts_ctx_hybrid_cum_rewards, linestyle='--')
plt.plot(ucb1_ctx_hybrid_cum_rewards, linestyle='--')
plt.legend(['Clairvoyant', 'Thompson sampling', 'UCB1', 'Thompson sampling + known context', 'UCB1 + known context', 
            'ThompsonSampling + context generation', 'UCB1 + context generation',
            'ThompsonSampling + context generation (gaussian bounds)', 'UCB1 + context generation (gaussian bounds)',
            'ThompsonSampling + context generation (hybrid bounds)', 'UCB1 + context generation (hybrid bounds)'],
            bbox_to_anchor = (1.05, 1), loc = 2)
plt.title('Total cumulative rewards')
plt.savefig(plot_path + 'cumulative_rewards.png', bbox_inches='tight', dpi = 300)
plt.close()

plt.plot([clairvoyant_cum_rewards[i] - ts_cum_rewards[i] for i in range(len(ts_cum_rewards))])
plt.plot([clairvoyant_cum_rewards[i] - ucb1_cum_rewards[i] for i in range(len(ucb1_cum_rewards))])
plt.plot([clairvoyant_cum_rewards[i] - ts_ctx_cum_rewards[i] for i in range(len(ts_ctx_cum_rewards))])
plt.plot([clairvoyant_cum_rewards[i] - ucb1_ctx_cum_rewards[i] for i in range(len(ucb1_ctx_cum_rewards))])
plt.legend(['Thompson sampling', 'UCB1', 'ThompsonSampling + context generation', 
            'UCB1 + context generation'], bbox_to_anchor = (1.05, 1), loc = 2)
plt.title('Total cumulative regret')
plt.savefig(plot_path + 'cumulative_regret.png', bbox_inches='tight', dpi = 300)
plt.close()

plt.plot([(clairvoyant_cum_rewards[i] - ts_cum_rewards[i]) / (i+1) for i in range(len(ts_cum_rewards))])
plt.plot([(clairvoyant_cum_rewards[i] - ucb1_cum_rewards[i]) / (i+1) for i in range(len(ucb1_cum_rewards))])
plt.plot([(clairvoyant_cum_rewards[i] - ts_ctx_cum_rewards[i]) / (i+1) for i in range(len(ts_ctx_cum_rewards))])
plt.plot([(clairvoyant_cum_rewards[i] - ucb1_ctx_cum_rewards[i]) / (i+1) for i in range(len(ucb1_ctx_cum_rewards))])
plt.legend(['Thompson sampling', 'UCB1', 'ThompsonSampling + context generation', 
            'UCB1 + context generation'], bbox_to_anchor = (1.05, 1), loc = 2)
plt.title('Total average regret')
plt.savefig(plot_path + 'average_regret.png', bbox_inches='tight', dpi = 300)
plt.close()

###############################################
# Plotting monitoring data
###############################################

ts_matching_sizes = ts_monitor.get_matching_sizes()['per_day']
plt.plot(ts_matching_sizes)
ucb1_matching_sizes = ucb1_monitor.get_matching_sizes()['per_day']
plt.plot(ucb1_matching_sizes)
plt.legend(['Thompson sampling', 'UCB1'], bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Matching sizes")
plt.savefig(plot_path + 'matching_sizes.png', bbox_inches='tight', dpi = 300)
plt.close()

plt.plot(np.cumsum(ts_matching_sizes) / np.linspace(1, num_days, num_days))
plt.plot(np.cumsum(ucb1_matching_sizes) / np.linspace(1, num_days, num_days))
plt.legend(['Thompson sampling', 'UCB1'], bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Average matching sizes")
plt.savefig(plot_path + 'average_matching_sizes.png', bbox_inches='tight', dpi = 300)
plt.close()

ts_full_matching_sizes = ts_monitor.get_matching_sizes(type = 'full_matching_edges')['per_day']
plt.plot(ts_full_matching_sizes)
ucb1_full_matching_sizes = ucb1_monitor.get_matching_sizes(type = 'full_matching_edges')['per_day']
plt.plot(ucb1_full_matching_sizes)
plt.legend(['Thompson sampling', 'UCB1'], bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Full matching sizes")
plt.savefig(plot_path + 'full_matching_sizes.png', bbox_inches='tight', dpi = 300)
plt.close()

plt.plot(np.cumsum(ts_full_matching_sizes) / np.linspace(1, num_days, num_days))
plt.plot(np.cumsum(ucb1_full_matching_sizes) / np.linspace(1, num_days, num_days))
plt.legend(['Thompson sampling', 'UCB1'], bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Average full matching sizes")
plt.savefig(plot_path + 'average_full_matching_sizes.png', bbox_inches='tight', dpi = 300)
plt.close()

plt.plot(ts_monitor.get_graph_sizes()['pre_matching']['per_day'])
plt.plot(ts_monitor.get_graph_sizes()['post_matching']['per_day'])
plt.plot(ucb1_monitor.get_graph_sizes()['pre_matching']['per_day'])
plt.plot(ucb1_monitor.get_graph_sizes()['post_matching']['per_day'])
plt.legend(['Thompson sampling - Pre-matching', 'Thompson sampling - Post-matching',
            'UCB1 - Pre-matching', 'UCB1 - Post-matching'], bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Graph sizes")
plt.savefig(plot_path + 'graph_sizes.png', bbox_inches='tight', dpi = 300)
plt.close()

legend = []
ts_rewards_per_arm = ts_monitor.get_rewards_per_arm()['per_day']
for (arm, rewards) in ts_rewards_per_arm.items():
    plt.plot(np.cumsum(rewards))
    legend.append('Thompson sampling - arm ' + str(arm))
plt.gca().set_prop_cycle(None)
ucb1_rewards_per_arm = ucb1_monitor.get_rewards_per_arm()['per_day']
for (arm, rewards) in ucb1_rewards_per_arm.items():
    plt.plot(np.cumsum(rewards), linestyle='dashed')
    legend.append('UCB1 - arm ' + str(arm))
plt.gca().set_prop_cycle(None)
ts_known_ctx_rewards_per_arm = ts_known_ctx_monitor.get_rewards_per_arm()['per_day']
for (arm, rewards) in ts_known_ctx_rewards_per_arm.items():
    plt.plot(np.cumsum(rewards), linestyle='-.')
    legend.append('Thompson sampling (known context) - arm ' + str(arm))
plt.gca().set_prop_cycle(None)
ucb1_known_ctx_rewards_per_arm = ucb1_known_ctx_monitor.get_rewards_per_arm()['per_day']
for (arm, rewards) in ucb1_known_ctx_rewards_per_arm.items():
    plt.plot(np.cumsum(rewards), linestyle=':')
    legend.append('UCB1 (known context) - arm ' + str(arm))
plt.legend(legend, bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Rewards per arm")
plt.savefig(plot_path + 'rewards_per_arm.png', bbox_inches='tight', dpi = 300)
plt.close()

legend = []
ts_pulls_per_arm = ts_monitor.get_number_of_arm_pulls()['per_day']
for (arm, n_pulls) in ts_pulls_per_arm.items():
    plt.plot(np.cumsum(n_pulls))
    legend.append('Thompson sampling - arm ' + str(arm))
plt.gca().set_prop_cycle(None)
ucb1_pulls_per_arm = ucb1_monitor.get_number_of_arm_pulls()['per_day']
for (arm, n_pulls) in ucb1_pulls_per_arm.items():
    plt.plot(np.cumsum(n_pulls), linestyle='dashed')
    legend.append('UCB1 - arm ' + str(arm))
plt.gca().set_prop_cycle(None)
ts_known_ctx_pulls_per_arm = ts_known_ctx_monitor.get_number_of_arm_pulls()['per_day']
for (arm, n_pulls) in ts_known_ctx_pulls_per_arm.items():
    plt.plot(np.cumsum(n_pulls), linestyle='-.')
    legend.append('Thompson sampling (known context) - arm ' + str(arm))
plt.gca().set_prop_cycle(None)
ucb1_known_ctx_pulls_per_arm = ucb1_known_ctx_monitor.get_number_of_arm_pulls()['per_day']
for (arm, n_pulls) in ucb1_known_ctx_pulls_per_arm.items():
    plt.plot(np.cumsum(n_pulls), linestyle=':')
    legend.append('UCB1 (known context) - arm ' + str(arm))
plt.legend(legend, bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Number of pulls per arm")
plt.savefig(plot_path + 'pulls_per_arm.png', bbox_inches='tight', dpi = 300)
plt.close()

ts_total_pulls = np.zeros(num_days)
for (_, n_pulls) in ts_pulls_per_arm.items():
    ts_total_pulls += np.cumsum(n_pulls)
plt.plot(ts_total_pulls)
ucb1_total_pulls = np.zeros(num_days)
for (_, n_pulls) in ucb1_pulls_per_arm.items():
    ucb1_total_pulls += np.cumsum(n_pulls)
plt.plot(ucb1_total_pulls)
plt.legend(['Thompson sampling', 'UCB1'], bbox_to_anchor = (1.05, 1), loc = 2)
plt.title("Total number of pulls")
plt.savefig(plot_path + 'total_arm_pulls.png', bbox_inches='tight', dpi = 300)
plt.close()

ts_ctx_rewards_per_arm = ts_ctx_monitor.get_rewards_per_arm()['per_day']
ts_ctx_pulls_per_arm = ts_ctx_monitor.get_number_of_arm_pulls()['per_day']
ucb1_ctx_rewards_per_arm = ucb1_ctx_monitor.get_rewards_per_arm()['per_day']
ucb1_ctx_pulls_per_arm = ucb1_ctx_monitor.get_number_of_arm_pulls()['per_day']

left_classes_ids = [c.id for c in environment.classes[0] if c.is_left]
right_classes_ids = [c.id for c in environment.classes[0] if not c.is_left]
for l_id in left_classes_ids:
    for r_id in right_classes_ids:
        arm = (l_id, r_id)
        plt.subplot(len(left_classes_ids), len(right_classes_ids), 1 + l_id * len(right_classes_ids) + r_id - len(left_classes_ids), title = "Arm " + str(arm))
        plt.plot(np.cumsum(ts_rewards_per_arm[arm]) / np.maximum(np.cumsum(ts_pulls_per_arm[arm]), 1))
        plt.plot(np.cumsum(ucb1_rewards_per_arm[arm]) / np.maximum(np.cumsum(ucb1_pulls_per_arm[arm]), 1))
        plt.plot(np.cumsum(ts_known_ctx_rewards_per_arm[arm]) / np.maximum(np.cumsum(ts_known_ctx_pulls_per_arm[arm]), 1))
        plt.plot(np.cumsum(ucb1_known_ctx_rewards_per_arm[arm]) / np.maximum(np.cumsum(ucb1_known_ctx_pulls_per_arm[arm]), 1))
        plt.plot(np.cumsum(ts_ctx_rewards_per_arm[arm]) / np.maximum(np.cumsum(ts_ctx_pulls_per_arm[arm]), 1))
        plt.plot(np.cumsum(ucb1_ctx_rewards_per_arm[arm]) / np.maximum(np.cumsum(ucb1_ctx_pulls_per_arm[arm]), 1))
plt.legend(['Thompson sampling', 'UCB1', 'Thompson sampling (known context)', 
            'UCB1 (known context)', 'Thompson sampling + context generation', 'UCB1 + context generation'], 
            bbox_to_anchor = (1.05, 1), loc = 2)
plt.savefig(plot_path + 'average_rewards_per_arm.png', bbox_inches='tight', dpi = 300)
plt.close()