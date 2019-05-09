try:
    # IMPORT FOR PYCHARM USERS
    from matching.graph.graph import Graph
    from matching.experiment.class_algo import Class_Algo
    from matching.experiment.class_algo_edge import Class_Algo_Edge

    from matching.environment.class_env import Class_Env
    from matching.environment.class_env_edge import Class_Env_Edge
    from matching.environment.environment import Environment
    from matching.environment.restorable_environment import RestorableEnvironment

    from matching.distributions.beta import Beta
    from matching.distributions.uniform_discrete import Uniform_Discrete
    from matching.distributions.bernoulli import Bernoulli
    from matching.distributions.gaussian import Gaussian
    from matching.distributions.UCB1 import UCB1

    from matching.experiment.DDA import DDA
    from matching.algorithms.Hungarian_algorithm import Hungarian_algorithm

    from matching.config.random_config import get_configuration as get_random_configuration
    from matching.config.test_config import get_configuration as get_test_configuration

    # from matching.utilities.drawing import draw_graph
    from random import randint, random
except (SystemError, ImportError):
    # IMPORT FOR NON-PYCHARM USERS

    from graph import Graph
    
    from experiment.class_algo import Class_Algo
    from experiment.class_algo_edge import Class_Algo_Edge
    
    from environment.class_env import Class_Env
    from environment.class_env_edge import Class_Env_Edge
    from environment.environment import Environment
    from environment.restorable_environment import RestorableEnvironment
    
    from distributions import Beta
    from distributions import Uniform_Discrete
    from distributions import Bernoulli
    from distributions import Gaussian
    from distributions import UCB1

    from experiment.DDA import DDA
    from algorithms.Hungarian_algorithm import Hungarian_algorithm

    from config.random_config import get_configuration as get_random_configuration
    from config.test_config import get_configuration as get_test_configuration
    
    from utilities.drawing import draw_graph
    from random import randint, random

    import matplotlib.pyplot as plt

from enum import Enum
import math

###############################################
# Configurations
###############################################

num_days = 5    # Number of days the experiment is run

###############################################
# Build environment (from config file)
###############################################

env_classes = []
phase_lengths = []

configuration = get_test_configuration()
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

print(env_classes)

###############################################
# Perform loop function (built to be reusable as much as possible)
###############################################

class LearnerType(Enum):
    ThompsonSampling = 0
    UCB1 = 1
    Clairvoyant = 2

def perform_experiment(environment, num_days, phase_lengths, learner_type, context_structure = None):
    print("\n--------- Starting experiment with " + learner_type.name + " ---------")

    ###############################################
    # Setup the experiment
    ###############################################

    # Setup the context
    day_length = sum(phase_lengths)
    if context_structure == None:
        context_structure = [ day_length ]

    # Instatiate DDA class with the selected matching algorithm
    Dda = DDA(Hungarian_algorithm())

    # Instantiate the main Graph
    graph = Graph()

    # Build the Class_Algos from the ids of the Class_Envs
    contextualized_algo_classes = {} # Dictionary to map rounds to corresponding algo_class (when using context)
    for (context_id, context) in enumerate(context_structure):
        left_classes_ids = [c.id for c in environment.classes[0] if c.is_left]
        right_classes_ids = [c.id for c in environment.classes[0] if not c.is_left]

        algo_classes = [Class_Algo(id, True) for id in left_classes_ids] + [Class_Algo(id, False) for id in right_classes_ids]

        for i in left_classes_ids:
            for j in right_classes_ids:
                distribution = Beta() if learner_type == LearnerType.ThompsonSampling else UCB1()
                class_edge = Class_Algo_Edge(distribution)
                l_class = [c for c in algo_classes if c.id == i][0]
                r_class = [c for c in algo_classes if c.id == j][0]
                l_class.set_edge_data(r_class, class_edge)
                r_class.set_edge_data(l_class, class_edge)

        for i in range(context):
            round_id = i + sum(context_structure[:context_id])
            contextualized_algo_classes[round_id] = algo_classes

    ###############################################
    # Utility functions (NOTE: some are implemented as clojures)
    ###############################################

    def get_algo_class(class_id, round_id):
        return [c for c in contextualized_algo_classes[round_id] if c.id == class_id][0]

    def get_env_class(class_id, phase_id):
        return [c for c in env_classes[phase_id] if c.id == class_id][0]

    def update_UCB1_current_time(iteration_number):
        for c in algo_classes:
            for ed in c.edge_data.values():
                ed.distribution.current_time = iteration_number

    ###############################################
    # Main experiment loop
    ###############################################

    rewards_by_day = []
    all_rewards = []

    iteration_number = 0

    for day in range(num_days): # For every day the experiment is run
        print("------ Day " + str(day + 1) + " ------")

        day_rewards = []

        for (phase_id, phase_length) in enumerate(phase_lengths):   # For every phase of the day
            # print("---- Phase " + str(phase_id + 1) + " ----")

            phase_rewards = []

            for round_id in range(phase_length):   # For every round in the phase
                # print("-- Round " + str(round + 1) + " --")

                iteration_number += 1
                round_reward = 0

                # Sample new nodes from the environment
                new_nodes = environment.get_new_nodes(phase_id)

                # Add those new nodes to the graph (mapping the id returned by the environment into the correct Class_Algo)
                for (class_id, time_to_stay) in new_nodes:
                    node_class = get_algo_class(class_id, round_id)
                    graph.add_node(node_class, time_to_stay)

                # Update the estimates of the weights of the graph
                if learner_type == LearnerType.ThompsonSampling:
                    # beta sample
                    graph.update_weights()
                elif learner_type == LearnerType.UCB1:
                    # UCB1 bound
                    update_UCB1_current_time(iteration_number)
                    graph.update_weights()
                elif learner_type == LearnerType.Clairvoyant:
                    # Update the clairvoyant graph with the real weights
                    for edge in graph.edges:
                        node1_env_class = get_env_class(edge.node1.node_class.id, phase_id)
                        edge_data = node1_env_class.edge_data[edge.node2.node_class.id]
                        edge.weight = edge_data.weight_distribution.p * edge_data.constant_weight

                # Whenever a node is going to exit the experiment run the DDA (Deferred Dynamic Acceptance) algorithm
                if len(graph.edges) > 0 and Dda.is_there_critical_node(graph.nodes):
                    matching_edges = Dda.perform_matching(graph)

                    # Given the results of DDA (if and what nodes to match), actually perform the matching
                    for edge in matching_edges:
                        # Draw rewards and update distributions for each matching performed
                        matching_result, matching_weight = environment.get_reward(edge.node1.node_class.id, edge.node2.node_class.id, phase_id)
                        
                        #print("Pulling arm " + str((edge.node1.node_class.id, edge.node2.node_class.id)) + " and getting reward " + str((matching_result, matching_weight)))

                        if learner_type in [ LearnerType.ThompsonSampling, LearnerType.UCB1 ]:
                            reward = matching_result * matching_weight
                        elif learner_type == LearnerType.Clairvoyant:
                            reward = edge.weight
                        round_reward += reward

                        node1_class = get_algo_class(edge.node1.node_class.id, round_id)
                        edge_data = node1_class.edge_data[edge.node2.node_class.id]

                        if learner_type == LearnerType.ThompsonSampling:
                            # TS update
                            edge_data.distribution.update_parameters([matching_result, 1 - matching_result])
                        elif learner_type == LearnerType.UCB1:
                            # UCB1 update
                            edge_data.distribution.update_parameters(matching_result)

                        # Update estimate of constant weight
                        edge_data.update_estimated_weight(matching_weight)

                        # Remove matched nodes from the graph
                        graph.remove_node(edge.node1)
                        graph.remove_node(edge.node2)

                # Run the end_round routine of the graph, to update the time_to_stay for each node
                graph.end_round_routine()

                phase_rewards.append(round_reward)
                all_rewards.append(round_reward)

            # End of phase
            day_rewards.append(phase_rewards)

        # End of day
        rewards_by_day.append(day_rewards)

    return (all_rewards, rewards_by_day)

###############################################
# Run experiments
###############################################

ts_rewards, _ = perform_experiment(environment, num_days, phase_lengths, LearnerType.ThompsonSampling)
environment.restore() # Restore the environment (so that randomization doesn't affect different algorithms)
ucb1_rewards, _ = perform_experiment(environment, num_days, phase_lengths, LearnerType.UCB1)
environment.restore() # Restore the environment (so that randomization doesn't affect different algorithms)
clairvoyant_rewards, _ = perform_experiment(environment, num_days, phase_lengths, LearnerType.Clairvoyant)

###############################################
# Plotting
###############################################

ts_cum_rewards = [sum(ts_rewards[:i]) for i in range(len(ts_rewards))]
ucb1_cum_rewards = [sum(ucb1_rewards[:i]) for i in range(len(ucb1_rewards))]
clairvoyant_cum_rewards = [sum(clairvoyant_rewards[:i]) for i in range(len(clairvoyant_rewards))]

plt.plot(ts_cum_rewards)
plt.plot(ucb1_cum_rewards)
plt.plot(clairvoyant_cum_rewards)
plt.legend(['Thompson sampling', 'UCB1', 'Clairvoyant'], bbox_to_anchor = (0.05, 1), loc = 2)
plt.title('Total cumulative rewards')
plt.show()

plt.plot([clairvoyant_cum_rewards[i] - ts_cum_rewards[i] for i in range(len(ts_cum_rewards))])
plt.plot([clairvoyant_cum_rewards[i] - ucb1_cum_rewards[i] for i in range(len(ucb1_cum_rewards))])
plt.legend(['Thompson sampling', 'UCB1'], bbox_to_anchor = (0.05, 1), loc = 2)
plt.title('Total cumulative regret')
plt.show()

plt.plot([(clairvoyant_cum_rewards[i] - ts_cum_rewards[i]) / (i+1) for i in range(len(ts_cum_rewards))])
plt.plot([(clairvoyant_cum_rewards[i] - ucb1_cum_rewards[i]) / (i+1) for i in range(len(ucb1_cum_rewards))])
plt.legend(['Thompson sampling', 'UCB1'], bbox_to_anchor = (0.05, 1), loc = 2)
plt.title('Total average regret')
plt.show()