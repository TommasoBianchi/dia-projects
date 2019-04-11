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
    
    from utilities.drawing import draw_graph
    from random import randint, random

###############################################
# Configurations (for now, kinda random)
###############################################

num_days = 1    # Number of days the experiment is run
phase_lengths = [6] # Duration of each phase in round (phases restart identically each day)
num_phases = len(phase_lengths)
num_left_classes = 2
num_right_classes = 1

###############################################
# Build environment
###############################################

env_classes = []
for _ in range(num_phases):
    phase_env_classes = []

    for id in range(num_left_classes):
        phase_env_classes.append(Class_Env(id, True, Gaussian(2, 1), Uniform_Discrete(1, 3)))

    for id in range(num_right_classes):
        phase_env_classes.append(
            Class_Env(num_right_classes + id + 1, False, Gaussian(2, 1), Uniform_Discrete(2, 5)))

    for i in range(num_left_classes):
        for j in range(num_right_classes):
            class_edge = Class_Env_Edge(Bernoulli(random()), randint(1, 10))
            l_class = [c for c in phase_env_classes if c.id == i][0]
            r_class = [c for c in phase_env_classes if c.id == j + num_right_classes + 1][0]
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

for day in range(num_days): # For every day the experiment is run
    print("------ Day " + str(day + 1) + " ------")
    for (phase_id, phase_length) in enumerate(phase_lengths):   # For every phase of the day
        print("---- Phase " + str(phase_id + 1) + " ----")
        for round in range(phase_length):   # For every round in the phase
            print("-- Round " + str(round + 1) + " --")

            # Sample new nodes from the environment
            new_nodes = environment.get_new_nodes(phase_id)

            # Add those new nodes to the graph (mapping the id returned by the environment into the correct Class_Algo)
            for (class_id, time_to_stay) in new_nodes:
                node_class = [c for c in algo_classes if c.id == class_id][0]
                graph.add_node(node_class, time_to_stay)

            # Update the estimates of the weights of the graph (i.e. beta sample/UCB1 bound)
            graph.update_weights()

            # Draw the graph (for debugging)
            #draw_graph(graph)

            # Whenever a node is going to exit the experiment run the DDA (Deferred Dynamic Acceptance) algorithm
            if len(graph.edges) > 0 and Dda.is_there_critical_seller_node(graph.nodes):
                print("Calling DDA")
                # matching_assignment, updated_graph = Dda.perform_matching(graph)
                # graph = updated_graph
                #
                print("Assignment found")

                # TODO: given the results of DDA (if and what nodes to match), actually perform the matching
                # TODO: draw rewards and update distributions for each matching performed
                # TODO: remove matched nodes from the graph

                # edges = graph.get_edges_from_matching(matching_assignment)

                # print(matching_assignment)
                # print(edges)

            # Run the end_round routine of the graph, to update the time_to_stay for each node
            graph.end_round_routine()
