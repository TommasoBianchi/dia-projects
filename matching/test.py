try:
    # IMPORT FOR PYCHARM USERS
    from matching.graph.graph import Graph
    from matching.experiment.class_algo import Class_Algo
    from matching.experiment.class_algo_edge import Class_Algo_Edge

    from matching.environment.class_env import Class_Env
    from matching.environment.class_env_edge import Class_Env_Edge
    from matching.environment.environment import Environment

    from matching.distributions.beta import Beta
    from matching.distributions.uniform_discrete import Uniform_Discrete
    from matching.distributions.bernoulli import Bernoulli
    from matching.distributions.gaussian import Gaussian

    from matching.experiment.DDA import DDA
    from matching.algorithms.Hungarian_algorithm import Hungarian_algorithm

    from matching.config.random_config import get_configuration

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
    
    from distributions import Beta
    from distributions import Uniform_Discrete
    from distributions import Bernoulli
    from distributions import Gaussian

    from experiment.DDA import DDA
    from algorithms.Hungarian_algorithm import Hungarian_algorithm

    from config.random_config import get_configuration
    
    from utilities.drawing import draw_graph
    from random import randint, random

    import matplotlib.pyplot as plt

import math

###############################################
# Configurations
###############################################

num_days = 10    # Number of days the experiment is run

###############################################
# Build environment (from config file)
###############################################

env_classes = []
phase_lengths = []

configuration = get_configuration() # NOTE: for now this generate a random configuration
for phase_data in configuration['phase_data']:
    phase_lengths.append(phase_data['duration'])
    phase_env_classes = []

    for (id, ldata) in enumerate(phase_data['left_classes']):
        phase_env_classes.append(Class_Env(id, True, 
                                           Gaussian(ldata['new_node_rate_mean'], ldata['new_node_rate_variance']), 
                                           Uniform_Discrete(ldata['time_to_stay_min'], ldata['time_to_stay_max'])))
    num_left_classes = len(phase_data['left_classes'])
    for (id, ldata) in enumerate(phase_data['right_classes']):
        phase_env_classes.append(Class_Env(id + num_left_classes + 1, False, 
                                           Gaussian(ldata['new_node_rate_mean'], ldata['new_node_rate_variance']), 
                                           Uniform_Discrete(ldata['time_to_stay_min'], ldata['time_to_stay_max'])))
    for (ids, edge_data) in phase_data['edge_data'].items():
        class_edge = Class_Env_Edge(Bernoulli(edge_data['mean']), edge_data['weight'])
        l_class = [c for c in phase_env_classes if c.id == ids[0]][0]
        r_class = [c for c in phase_env_classes if c.id == ids[1] + num_left_classes + 1][0]
        l_class.set_edge_data(r_class, class_edge)
        r_class.set_edge_data(l_class, class_edge)

    env_classes.append(phase_env_classes)

environment = Environment(env_classes)

###############################################
# Setup the experiment
###############################################

# Instatiate DDA class with the selected matching algorithm
Dda = DDA(Hungarian_algorithm())

# Instantiate the main Graph
graph = Graph()
# Instantiate the clairvoyant Graph
clairvoyant_graph = Graph()

# Build the Class_Algos from the ids of the Class_Envs
left_classes_ids = [c.id for c in env_classes[0] if c.is_left]
right_classes_ids = [c.id for c in env_classes[0] if not c.is_left]

algo_classes = [Class_Algo(id, True) for id in left_classes_ids] + [Class_Algo(id, False) for id in right_classes_ids]

for i in left_classes_ids:
    for j in right_classes_ids:
        class_edge = Class_Algo_Edge(Beta())
        l_class = [c for c in algo_classes if c.id == i][0]
        r_class = [c for c in algo_classes if c.id == j][0]
        l_class.set_edge_data(r_class, class_edge)
        r_class.set_edge_data(l_class, class_edge)

###############################################
# Main experiment loop
###############################################

rewards_by_day = []
all_rewards = []

clairvoyant_all_rewards = []

for day in range(num_days): # For every day the experiment is run
    print("------ Day " + str(day + 1) + " ------")

    day_rewards = []

    for (phase_id, phase_length) in enumerate(phase_lengths):   # For every phase of the day
        # print("---- Phase " + str(phase_id + 1) + " ----")

        phase_rewards = []

        for round in range(phase_length):   # For every round in the phase
            # print("-- Round " + str(round + 1) + " --")

            round_reward = 0
            round_clairvoyant_reward = 0

            # Sample new nodes from the environment
            new_nodes = environment.get_new_nodes(phase_id)

            # Add those new nodes to the graph (mapping the id returned by the environment into the correct Class_Algo)
            for (class_id, time_to_stay) in new_nodes:
                node_class = [c for c in algo_classes if c.id == class_id][0]
                graph.add_node(node_class, time_to_stay)

                clairvoyant_graph.add_node(node_class, time_to_stay)

            # Update the estimates of the weights of the graph (i.e. beta sample/UCB1 bound)
            graph.update_weights()

            # Update the clairvoyant graph with the real weights
            for edge in clairvoyant_graph.edges:
                node1_env_class = [c for c in env_classes[phase_id] if c.id == edge.node1.node_class.id][0]
                edge_data = node1_env_class.edge_data[edge.node2.node_class.id]
                edge.weight = edge_data.weight_distribution.p * edge_data.constant_weight

            # Draw the graph (for debugging)
            #draw_graph(graph)

            # Whenever a node is going to exit the experiment run the DDA (Deferred Dynamic Acceptance) algorithm
            if len(graph.edges) > 0 and Dda.is_there_critical_seller_node(graph.nodes):
                # print("Calling DDA")
                matching_edges, updated_graph = Dda.perform_matching(graph)
                graph = updated_graph
                #
                # print("Assignment found")

                # Given the results of DDA (if and what nodes to match), actually perform the matching
                for edge in matching_edges:
                    # Draw rewards and update distributions for each matching performed
                    matching_result, matching_weight = environment.get_reward(edge.node1.node_class.id, edge.node2.node_class.id, phase_id)
                    
                    reward = matching_result * matching_weight
                    round_reward += reward

                    node1_class = [c for c in algo_classes if c.id == edge.node1.node_class.id][0]
                    edge_data = node1_class.edge_data[edge.node2.node_class.id]

                    # TS update
                    edge_data.distribution.update_parameters([edge_data.distribution.alpha + matching_result,
                                                             edge_data.distribution.beta + (1 - matching_result)])
                    if edge_data.weight_estimation_samples == 0:
                        edge_data.estimated_weight = matching_weight
                    else:
                        edge_data.estimated_weight += (matching_weight - edge_data.estimated_weight) / edge_data.weight_estimation_samples
                    edge_data.weight_estimation_samples += 1

                    # TODO: UCB1 update

                    # Remove matched nodes from the graph
                    graph.remove_node(edge.node1)
                    graph.remove_node(edge.node2)

            if len(clairvoyant_graph.edges) > 0 and Dda.is_there_critical_seller_node(clairvoyant_graph.nodes):
                matching_edges, updated_graph = Dda.perform_matching(clairvoyant_graph)
                clairvoyant = updated_graph

                # Given the results of DDA (if and what nodes to match), actually perform the matching
                for edge in matching_edges:
                    # Draw rewards and update distributions for each matching performed
                    matching_result, matching_weight = environment.get_reward(edge.node1.node_class.id, edge.node2.node_class.id, phase_id)
                    
                    reward = matching_result * matching_weight
                    round_clairvoyant_reward += reward

                    # Remove matched nodes from the graph
                    clairvoyant_graph.remove_node(edge.node1)
                    clairvoyant_graph.remove_node(edge.node2)

            # Run the end_round routine of the graph, to update the time_to_stay for each node
            graph.end_round_routine()

            clairvoyant_graph.end_round_routine()

            phase_rewards.append(round_reward)
            all_rewards.append(round_reward)

            clairvoyant_all_rewards.append(round_clairvoyant_reward)

        # End of phase
        day_rewards.append(phase_rewards)

    # End of day
    rewards_by_day.append(day_rewards)

# Plotting

cum_rewards = [sum(all_rewards[:i]) for i in range(len(all_rewards))]
cum_clairvoyant_rewards = [sum(clairvoyant_all_rewards[:i]) for i in range(len(clairvoyant_all_rewards))]

# print(all_rewards)
# print(clairvoyant_all_rewards)

plt.plot(cum_rewards)
plt.plot(cum_clairvoyant_rewards)
plt.legend(['Thompson sampling', 'Clairvoyant'])
plt.title('Total cumulative rewards')
plt.show()

plt.plot([cum_clairvoyant_rewards[i] - cum_rewards[i] for i in range(len(cum_rewards))])
plt.title('Total cumulative regret')
plt.show()

plt.plot([(cum_clairvoyant_rewards[i] - cum_rewards[i]) / (i+1) for i in range(len(cum_rewards))])
plt.title('Total average regret')
plt.show()