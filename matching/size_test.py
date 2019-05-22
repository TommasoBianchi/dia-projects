from environment.class_env import Class_Env
from environment.class_env_edge import Class_Env_Edge
from environment.environment import Environment

from distributions import Uniform_Discrete
from distributions import Bernoulli
from distributions import Gaussian
from distributions import Beta

from graph.graph import Graph

from experiment.class_algo import Class_Algo
from experiment.class_algo_edge import Class_Algo_Edge

from config.random_config import get_configuration as get_random_configuration
from config.test_config import get_configuration as get_test_configuration
from config.test_multiphase_config import get_configuration as get_test_multiphase_configuration

import matplotlib.pyplot as plt

num_days = 100    # Number of days the experiment is run

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

environment = Environment(env_classes)

# ------------------------------------ 

# Instantiate the main Graph
graph = Graph()

day_length = sum(phase_lengths)
context_structure = [ day_length ]
contextualized_algo_classes = {} # Dictionary to map rounds to corresponding algo_class (when using context)
for (context_id, context) in enumerate(context_structure):
    left_classes_ids = [c.id for c in environment.classes[0] if c.is_left]
    right_classes_ids = [c.id for c in environment.classes[0] if not c.is_left]

    algo_classes = [Class_Algo(id, True) for id in left_classes_ids] + [Class_Algo(id, False) for id in right_classes_ids]

    for i in left_classes_ids:
        for j in right_classes_ids:
            class_edge = Class_Algo_Edge(Beta())
            l_class = [c for c in algo_classes if c.id == i][0]
            r_class = [c for c in algo_classes if c.id == j][0]
            l_class.set_edge_data(r_class, class_edge)
            r_class.set_edge_data(l_class, class_edge)

    for i in range(context):
        round_id = i + sum(context_structure[:context_id])
        contextualized_algo_classes[round_id] = algo_classes

def get_algo_class(contextualized_algo_classes, class_id, round_id):
    return [c for c in contextualized_algo_classes[round_id] if c.id == class_id][0]

node_count_per_iteration = []
edge_count_per_iteration = []

for day in range(num_days): # For every day the experiment is run
    print("------ Day " + str(day + 1) + " ------")

    for (phase_id, phase_length) in enumerate(phase_lengths):   # For every phase of the day
        # print("---- Phase " + str(phase_id + 1) + " ----")

        for _ in range(phase_length):   # For every round in the phase
            # print("-- Round " + str(round_id) + " --")

            # Sample new nodes from the environment
            new_nodes = environment.get_new_nodes(phase_id)

            # Add those new nodes to the graph (mapping the id returned by the environment into the correct Class_Algo)
            for (class_id, time_to_stay) in new_nodes:
                node_class = get_algo_class(contextualized_algo_classes, class_id, round_id)
                graph.add_node(node_class, time_to_stay)

            # Run the end_round routine of the graph, to update the time_to_stay for each node
            graph.end_round_routine()

            node_count_per_iteration.append(len(graph.nodes))
            edge_count_per_iteration.append(len(graph.edges))

plt.plot(node_count_per_iteration)
plt.plot([(i+0.5)*day_length for i in range(num_days)],
         [sum(node_count_per_iteration[i*day_length:(i+1)*day_length]) / day_length for i in range(num_days)])
plt.show()
plt.plot(edge_count_per_iteration)
plt.plot([(i+0.5)*day_length for i in range(num_days)],
         [sum(edge_count_per_iteration[i*day_length:(i+1)*day_length]) / day_length for i in range(num_days)])
plt.show()