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

    from matching.experiment.DDA import DDA
    from matching.algorithms.Hungarian_algorithm import Hungarian_algorithm

    from matching.utilities.drawing import draw_graph
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

    from experiment.DDA import DDA
    from algorithms.Hungarian_algorithm import Hungarian_algorithm
    
    from utilities.drawing import draw_graph
    from random import randint, random

# Build environment

num_phases = 4
num_left_classes = 2
num_right_classes = 1

env_classes = []
for _ in range(num_phases):
    phase_env_classes = []

    for id in range(num_left_classes):
        phase_env_classes.append(Class_Env(id, True, Uniform_Discrete(0, 2), Uniform_Discrete(1, 3)))

    for id in range(num_right_classes):
        phase_env_classes.append(
            Class_Env(num_right_classes + id + 1, False, Uniform_Discrete(0, 3), Uniform_Discrete(2, 5)))

    for i in range(num_left_classes):
        for j in range(num_right_classes):
            class_edge = Class_Env_Edge(Bernoulli(random()), randint(1, 10))
            l_class = [c for c in phase_env_classes if c.id == i][0]
            r_class = [c for c in phase_env_classes if c.id == j + num_right_classes + 1][0]
            l_class.set_edge_data(r_class, class_edge)
            r_class.set_edge_data(l_class, class_edge)

    env_classes.append(phase_env_classes)

environment = Environment(env_classes)

# Setup the experiment

# instatiate DDA class with the selected matching algorithm
Dda = DDA(Hungarian_algorithm())

graph = Graph()

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

for round in range(5):
    new_nodes = environment.get_new_nodes(0)

    for (class_id, time_to_stay) in new_nodes:
        node_class = [c for c in algo_classes if c.id == class_id][0]
        graph.add_node(node_class, time_to_stay)

    graph.update_weights()

    #	TODO: method to produce the adjacency matrix from the graph
    adjacency_matrix = [[]]

    if Dda.is_there_critical_seller_node(graph.nodes):
        pass
        #matching_result, matching_assignment = Dda.perform_matching(adjacency_matrix)

        # TODO: to_graph_method(adjacency_matrix)

    draw_graph(graph)

    graph.end_round_routine()
