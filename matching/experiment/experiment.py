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
                context_generation_every_day = -1, debug_info = False):
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

                    # Add those new nodes to the graph (mapping the id returned by the environment into the correct Class_Algo)
                    for (class_id, time_to_stay) in new_nodes:
                        node_class = get_algo_class(contextualized_algo_classes, class_id, round_id)
                        graph.add_node(node_class, time_to_stay)

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
                        matching_edges = Dda.perform_matching(graph)

                        # Given the results of DDA (if and what nodes to match), actually perform the matching
                        for edge in matching_edges:
                            # print("Matching " + str((edge.node1.node_class.id, edge.node2.node_class.id)))

                            # Draw rewards and update distributions for each matching performed
                            matching_result, matching_weight = self.environment.get_reward(edge.node1.node_class.id, edge.node2.node_class.id, phase_id)
                            
                            # print("Pulling arm " + str((edge.node1.node_class.id, edge.node2.node_class.id)) + " and getting reward " + str((matching_result, matching_weight)))

                            if learner_type in [ LearnerType.ThompsonSampling, LearnerType.UCB1 ]:
                                reward = matching_result * matching_weight
                            elif learner_type in [ LearnerType.Clairvoyant, LearnerType.ContextEvaluation ]:
                                reward = edge.weight
                            round_reward += reward

                            # Save contextualized reward
                            reward_context = (round_id, min(edge.node1.node_class.id, edge.node2.node_class.id),
                                              max(edge.node1.node_class.id, edge.node2.node_class.id))
                            if reward_context not in rewards_by_context:
                                rewards_by_context[reward_context] = []
                            rewards_by_context[reward_context].append((matching_result, matching_weight))

                            node1_class = get_algo_class(contextualized_algo_classes, edge.node1.node_class.id, round_id)
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
                    for round_id in range(day_length):
                        for left_id in left_classes_ids:
                            for right_id in right_classes_ids:
                                context = (round_id, min(left_id, right_id), max(left_id, right_id))

                                if context in rewards_by_context:
                                    rewards = rewards_by_context[context]
                                    bernoulli_rewards = list(map(lambda el: el[0], rewards))
                                    weight_rewards = list(map(lambda el: el[1], rewards))
                                    bernoulli_mean = sum(bernoulli_rewards) / len(bernoulli_rewards)
                                    weight_mean = sum(weight_rewards) / len(weight_rewards)
                                    hoeffding_bound = np.sqrt(-np.log(0.05) / (2 * len(bernoulli_rewards)))
                                    context_generation_exp.edge_lower_bounds[context] = weight_mean * (bernoulli_mean - hoeffding_bound)
                                else:
                                    context_generation_exp.edge_lower_bounds[context] = -1e12 # minus infinity

                    rewards = context_generation_exp.perform(day + 1, LearnerType.ContextEvaluation, context_structure)

                    return sum(rewards)

                best_context_structure = max(all_context_structures, key = evaluate_context_structure)

                if debug_info:
                    print("Best context structure is " + str(context_structure))

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

        return all_rewards