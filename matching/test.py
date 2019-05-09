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

    from matching.experiment.experiment import Experiment, LearnerType

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

    from experiment import Experiment, LearnerType

    import matplotlib.pyplot as plt

import time

###############################################
# Configurations
###############################################

num_days = 8    # Number of days the experiment is run

###############################################
# Build environment (from config file)
###############################################

env_classes = []
phase_lengths = []

configuration = get_random_configuration()
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

experiment = Experiment(environment, phase_lengths, min_phase_length = 3)

start_time = time.time()
clairvoyant_rewards = experiment.perform(num_days, LearnerType.Clairvoyant, debug_info = True)
print("Clairvoyant executed in " + str(time.time() - start_time) + " seconds")
start_time = time.time()
ts_rewards = experiment.perform(num_days, LearnerType.ThompsonSampling, debug_info = True)
print("TS executed in " + str(time.time() - start_time) + " seconds")
start_time = time.time()
ucb1_rewards = experiment.perform(num_days, LearnerType.UCB1, debug_info = True)
print("UCB1 executed in " + str(time.time() - start_time) + " seconds")
start_time = time.time()
ts_ctx_rewards = experiment.perform(num_days, LearnerType.ThompsonSampling,
                                    context_generation_every_day = 5, debug_info = True)
print("TS-context executed in " + str(time.time() - start_time) + " seconds")
start_time = time.time()
ucb1_ctx_rewards = experiment.perform(num_days, LearnerType.UCB1,
                                      context_generation_every_day = 5, debug_info = True)
print("UCB1-context executed in " + str(time.time() - start_time) + " seconds")

###############################################
# Plotting
###############################################

ts_cum_rewards = [sum(ts_rewards[:i]) for i in range(len(ts_rewards))]
ucb1_cum_rewards = [sum(ucb1_rewards[:i]) for i in range(len(ucb1_rewards))]
ts_ctx_cum_rewards = [sum(ts_ctx_rewards[:i]) for i in range(len(ts_ctx_rewards))]
ucb1_ctx_cum_rewards = [sum(ucb1_ctx_rewards[:i]) for i in range(len(ucb1_ctx_rewards))]
clairvoyant_cum_rewards = [sum(clairvoyant_rewards[:i]) for i in range(len(clairvoyant_rewards))]

plt.plot(ts_cum_rewards)
plt.plot(ucb1_cum_rewards)
plt.plot(ts_ctx_cum_rewards)
plt.plot(ucb1_ctx_cum_rewards)
plt.plot(clairvoyant_cum_rewards)
plt.legend(['Thompson sampling', 'UCB1', 'ThompsonSampling + context generation', 
            'UCB1 + context generation', 'Clairvoyant'], bbox_to_anchor = (0.05, 1), loc = 2)
plt.title('Total cumulative rewards')
plt.show()

plt.plot([clairvoyant_cum_rewards[i] - ts_cum_rewards[i] for i in range(len(ts_cum_rewards))])
plt.plot([clairvoyant_cum_rewards[i] - ucb1_cum_rewards[i] for i in range(len(ucb1_cum_rewards))])
plt.plot([clairvoyant_cum_rewards[i] - ts_ctx_cum_rewards[i] for i in range(len(ts_ctx_cum_rewards))])
plt.plot([clairvoyant_cum_rewards[i] - ucb1_ctx_cum_rewards[i] for i in range(len(ucb1_ctx_cum_rewards))])
plt.legend(['Thompson sampling', 'ThompsonSampling + context generation', 
            'UCB1 + context generation', 'UCB1'], bbox_to_anchor = (0.05, 1), loc = 2)
plt.title('Total cumulative regret')
plt.show()

plt.plot([(clairvoyant_cum_rewards[i] - ts_cum_rewards[i]) / (i+1) for i in range(len(ts_cum_rewards))])
plt.plot([(clairvoyant_cum_rewards[i] - ucb1_cum_rewards[i]) / (i+1) for i in range(len(ucb1_cum_rewards))])
plt.plot([(clairvoyant_cum_rewards[i] - ts_ctx_cum_rewards[i]) / (i+1) for i in range(len(ts_ctx_cum_rewards))])
plt.plot([(clairvoyant_cum_rewards[i] - ucb1_ctx_cum_rewards[i]) / (i+1) for i in range(len(ucb1_ctx_cum_rewards))])
plt.legend(['Thompson sampling', 'ThompsonSampling + context generation', 
            'UCB1 + context generation', 'UCB1'], bbox_to_anchor = (0.05, 1), loc = 2)
plt.title('Total average regret')
plt.show()