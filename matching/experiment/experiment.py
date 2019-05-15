try:
    # IMPORT FOR PYCHARM USERS

    from matching.graph.graph import Graph

    from matching.experiment.class_algo import Class_Algo
    from matching.experiment.class_algo_edge import Class_Algo_Edge

    from matching.distributions.beta import Beta
    from matching.distributions.UCB1 import UCB1

    from matching.experiment.DDA import DDA
    from matching.algorithms.Hungarian_algorithm import Hungarian_algorithm

    from matching.context_generation.context_generation import generate_context_structures

    from matching.utilities.monitoring import ExperimentMonitor

    # from matching.utilities.drawing import draw_graph
    from random import randint, random
except (SystemError, ImportError):
    # IMPORT FOR NON-PYCHARM USERS

    from graph import Graph
    
    from experiment.class_algo import Class_Algo
    from experiment.class_algo_edge import Class_Algo_Edge
    
    from distributions import Beta
    from distributions import UCB1

    from experiment.DDA import DDA
    from algorithms.Hungarian_algorithm import Hungarian_algorithm

    from context_generation.context_generation import generate_context_structures

    from utilities.monitoring import ExperimentMonitor

from enum import Enum
import numpy as np
import random

class LearnerType(Enum):
    ThompsonSampling = 0
    UCB1 = 1
    Clairvoyant = 2
    ContextEvaluation = 3

class Experiment():
    def __init__(self, environment, phase_lengths, min_phase_length, seed = 0):
        self.environment = environment
        self.phase_lengths = phase_lengths
        self.min_phase_length = min_phase_length
        self.seed = seed
        self.edge_lower_bounds = None # Used in context generation

        np.random.seed(self.seed)
        random.seed(self.seed)

    ###############################################
    # Perform loop function (built to be reusable as much as possible)
    ###############################################
    def perform(self, num_days, learner_type, context_structure = None, 
                context_generation_every_day = -1, debug_info = False, monitoring_on = True):
        if debug_info:
            print("\n--------- Starting experiment with " + learner_type.name + " ---------")

        self.environment.restore() # Restore the environment (so that randomization doesn't affect different algorithms)
        np.random.seed(self.seed)
        random.seed(self.seed)

        ###############################################
        # Setup the experiment
        ###############################################

        # Setup the context
        day_length = sum(self.phase_lengths)
        if context_structure == None:
            context_structure = [ day_length ]

        # Instatiate DDA class with the selected matching algorithm
        Dda = DDA(Hungarian_algorithm())

        # Instantiate the main Graph
        graph = Graph()

        # Setup the monitoring for the experiment
        monitor = ExperimentMonitor(num_days, day_length, monitoring_on)

        ###############################################
        # Utility functions (NOTE: some are implemented as clojures)
        ###############################################

        # Build the Class_Algos from the ids of the Class_Envs (given a context structure)
        def build_contextualized_algo_classes(context_structure):
            contextualized_algo_classes = {} # Dictionary to map rounds to corresponding algo_class (when using context)

            for (context_id, context) in enumerate(context_structure):
                left_classes_ids = [c.id for c in self.environment.classes[0] if c.is_left]
                right_classes_ids = [c.id for c in self.environment.classes[0] if not c.is_left]

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

            return contextualized_algo_classes

        def get_algo_class(contextualized_algo_classes, class_id, round_id):
            return [c for c in contextualized_algo_classes[round_id] if c.id == class_id][0]

        def get_env_class(class_id, phase_id):
            return [c for c in self.environment.classes[phase_id] if c.id == class_id][0]

        def update_UCB1_current_time(contextualized_algo_classes, iteration_number):
            for algo_classes in contextualized_algo_classes.values():
                for c in algo_classes:
                    for ed in c.edge_data.values():
                        ed.distribution.current_time = iteration_number

        ###############################################
        # Main experiment loop
        ###############################################

        contextualized_algo_classes = build_contextualized_algo_classes(context_structure)

        rewards_by_context = {} # Save all the reward data with context labels (i.e. round_id and class_id pair)
        all_rewards = []

        iteration_number = 0

        for day in range(num_days): # For every day the experiment is run
            if debug_info:
                print("------ Day " + str(day + 1) + " ------")

            round_id = 0

            for (phase_id, phase_length) in enumerate(self.phase_lengths):   # For every phase of the day
                # print("---- Phase " + str(phase_id + 1) + " ----")

                for _ in range(phase_length):   # For every round in the phase
                    # print("-- Round " + str(round_id) + " --")

                    iteration_number += 1
                    round_reward = 0

                    # Sample new nodes from the environment
                    new_nodes = self.environment.get_new_nodes(phase_id)

                    # Experiment monitoring
                    monitor.new_nodes_added(day, round_id, new_nodes)

                    # Add those new nodes to the graph (mapping the id returned by the environment into the correct Class_Algo)
                    for (class_id, time_to_stay) in new_nodes:
                        node_class = get_algo_class(contextualized_algo_classes, class_id, round_id)
                        graph.add_node(node_class, time_to_stay)

                    # Experiment monitoring
                    monitor.graph_size_pre_matching(day, round_id, len(graph.nodes), len(graph.edges))

                    # Update the distribution used by each edge to match the current context structure
                    if len(context_structure) > 1 and learner_type in [ LearnerType.ThompsonSampling, LearnerType.UCB1 ]:
                        for node in graph.nodes:
                            node_class = get_algo_class(contextualized_algo_classes, node.node_class.id, round_id)
                            node.node_class = node_class

                    # Update the estimates of the weights of the graph
                    if learner_type == LearnerType.ThompsonSampling:
                        # beta sample
                        graph.update_weights()
                    elif learner_type == LearnerType.UCB1:
                        # UCB1 bound
                        update_UCB1_current_time(contextualized_algo_classes, iteration_number)
                        graph.update_weights()
                    elif learner_type == LearnerType.Clairvoyant:
                        # Update the clairvoyant graph with the real weights
                        for edge in graph.edges:
                            node1_env_class = get_env_class(edge.node1.node_class.id, phase_id)
                            edge_data = node1_env_class.edge_data[edge.node2.node_class.id]
                            edge.weight = edge_data.weight_distribution.p * edge_data.constant_weight
                    elif learner_type == LearnerType.ContextEvaluation:
                        # Update the graph with the Hoeffding lower bound estimated from old data
                        for edge in graph.edges:
                            edge_context = (round_id, min(edge.node1.node_class.id, edge.node2.node_class.id),
                                            max(edge.node1.node_class.id, edge.node2.node_class.id))
                            lower_bound = self.edge_lower_bounds[edge_context]
                            edge.weight = lower_bound

                    # Whenever a node is going to exit the experiment run the DDA (Deferred Dynamic Acceptance) algorithm
                    if len(graph.edges) > 0 and Dda.is_there_critical_node(graph.nodes):
                        matching_edges, full_matching_edges = Dda.perform_matching(graph)

                        # Experiment monitoring
                        monitor.matching_performed(day, round_id, matching_edges, full_matching_edges)

                        # Given the results of DDA (if and what nodes to match), actually perform the matching
                        for edge in matching_edges:

                            if learner_type in [ LearnerType.ThompsonSampling, LearnerType.UCB1 ]:
                                
                                # Draw rewards and update distributions for each matching performed
                                matching_result, matching_weight = self.environment.get_reward(edge.node1.node_class.id, edge.node2.node_class.id, phase_id)
                                reward = matching_result * matching_weight

                                # Experiment monitoring
                                monitor.reward_collected(day, round_id, phase_id,
                                                         edge.node1.node_class.id, edge.node2.node_class.id, 
                                                         matching_result, matching_weight)
                                
                                # Save contextualized reward
                                reward_context = (round_id, min(edge.node1.node_class.id, edge.node2.node_class.id),
                                                  max(edge.node1.node_class.id, edge.node2.node_class.id))
                                if reward_context not in rewards_by_context:
                                    rewards_by_context[reward_context] = []
                                rewards_by_context[reward_context].append((matching_result, matching_weight))
                            
                            elif learner_type in [ LearnerType.Clairvoyant, LearnerType.ContextEvaluation ]:
                                # For clairvoyant algorithms there is no need to sample rewards from the environment
                                reward = edge.weight

                                # Experiment monitoring
                                monitor.reward_collected(day, round_id, phase_id,
                                                         edge.node1.node_class.id, edge.node2.node_class.id, 
                                                         1, reward)
                            
                            round_reward += reward

                            node1_class = get_algo_class(contextualized_algo_classes, edge.node1.node_class.id, round_id)
                            edge_data = node1_class.edge_data[edge.node2.node_class.id]

                            if learner_type == LearnerType.ThompsonSampling:
                                # TS update
                                edge_data.distribution.update_parameters([matching_result, 1 - matching_result])
                                # Update estimate of constant weight
                                edge_data.update_estimated_weight(matching_weight)
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

                    # Experiment monitoring
                    monitor.graph_size_post_matching(day, round_id, len(graph.nodes), len(graph.edges))

                    all_rewards.append(round_reward)

                    round_id += 1

                # End of phase

            # Context generation
            if context_generation_every_day > 0 and (day+1) % context_generation_every_day == 0:
                if debug_info:
                    print("----- Generating new optimal context structure -----")

                all_context_structures = generate_context_structures(day_length, self.min_phase_length)

                env_copy = self.environment.copy()
                context_generation_exp = Experiment(env_copy, self.phase_lengths, self.min_phase_length)

                def evaluate_context_structure(context_structure):
                    # Build lower bounds on expected reward per edge
                    left_classes_ids = [c.id for c in env_copy.classes[0] if c.is_left]
                    right_classes_ids = [c.id for c in env_copy.classes[0] if not c.is_left]
                    context_generation_exp.edge_lower_bounds = {}
                    for (context_id, context) in enumerate(context_structure):
                        for left_id in left_classes_ids:
                            for right_id in right_classes_ids:
                                rewards = []

                                for i in range(context):
                                    round_id = i + sum(context_structure[:context_id])
                                    context_key = (round_id, min(left_id, right_id), max(left_id, right_id))

                                    if context_key in rewards_by_context:
                                        rewards += rewards_by_context[context_key]

                                if len(rewards) > 0:
                                    # Hoeffding lower bound
                                    bernoulli_rewards = list(map(lambda el: el[0], rewards))
                                    weight_rewards = list(map(lambda el: el[1], rewards))
                                    bernoulli_mean = np.mean(bernoulli_rewards)
                                    weight_mean = np.mean(weight_rewards)
                                    hoeffding_bound = np.sqrt(-np.log(0.05) / (2 * len(bernoulli_rewards)))
                                    # Gaussian lower bound
                                    full_rewards = list(map(lambda el: el[0] * el[1], rewards))
                                    mean_reward = np.mean(full_rewards)
                                    reward_std = np.std(full_rewards)
                                    n = len(full_rewards)
                                    z = 1.96 # for a 95% confidence interval
                                    gaussian_bound = mean_reward - (z * (reward_std / np.sqrt(n)))
                                    # Gaussian lower bound on weight
                                    gaussian_weight_bound = weight_mean - (z * (np.std(weight_rewards) / np.sqrt(n)))

                                    #total_lower_bound = gaussian_bound
                                    total_lower_bound = weight_mean * (bernoulli_mean - hoeffding_bound)
                                    #total_lower_bound = gaussian_weight_bound * (bernoulli_mean - hoeffding_bound)
                                    total_lower_bound = max(0, total_lower_bound)
                                else:
                                    total_lower_bound = 0 # minus infinity

                                for i in range(context):
                                    round_id = i + sum(context_structure[:context_id])
                                    context_key = (round_id, min(left_id, right_id), max(left_id, right_id))
                                    context_generation_exp.edge_lower_bounds[context_key] = total_lower_bound

                    rewards, _ = context_generation_exp.perform(day + 1, LearnerType.ContextEvaluation, context_structure, monitoring_on = False)

                    if debug_info:
                        print("-- Context structure " + str(context_structure) + " has an expected reward of " + str(sum(rewards)))

                    return sum(rewards)

                best_context_structure = max(all_context_structures, key = evaluate_context_structure)

                if debug_info:
                    print("Best context structure is " + str(best_context_structure))

                # Experiment monitoring
                monitor.context_generation_performed(day, best_context_structure)

                contextualized_algo_classes = build_contextualized_algo_classes(best_context_structure)

                # Re-feed old data to the newly built algo_classes
                for ((round_id, left_class_id, right_class_id), results) in rewards_by_context.items():
                    for (matching_result, matching_weight) in results:
                        left_class = get_algo_class(contextualized_algo_classes, left_class_id, round_id)
                        edge_data = left_class.edge_data[right_class_id]

                        if learner_type == LearnerType.ThompsonSampling:
                            # TS update
                            edge_data.distribution.update_parameters([matching_result, 1 - matching_result])
                        elif learner_type == LearnerType.UCB1:
                            # UCB1 update
                            edge_data.distribution.update_parameters(matching_result)

                        edge_data.update_estimated_weight(matching_weight)

            # End of day

        # for round_id in range(day_length):
        #     print("Estimates for round " + str(round_id) + " are:")
        #     algo_classes = contextualized_algo_classes[round_id]
        #     left_classes = [a for a in algo_classes if a.is_left]
        #     right_classes = [a for a in algo_classes if not a.is_left]
        #     for l in left_classes:
        #         for r in right_classes:
        #             couple = (l.id, r.id)
        #             edge_data = l.edge_data[r.id]
        #             avg_sample = np.mean([edge_data.distribution.sample() for _ in range(100)])
        #             print(str(couple) + ": " + str(edge_data.estimated_weight * avg_sample))

        return all_rewards, monitor