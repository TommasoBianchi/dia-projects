from graph import Graph

from experiment.class_algo import Class_Algo
from experiment.class_algo_edge import Class_Algo_Edge

from environment.class_env import Class_Env
from environment.class_env_edge import Class_Env_Edge
from environment.environment import Environment

from distributions import Beta
from distributions import Uniform_Discrete
from distributions import Bernoulli

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
		phase_env_classes.append(Class_Env(num_right_classes + id + 1, False, Uniform_Discrete(0, 3), Uniform_Discrete(2, 5)))

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

	draw_graph(graph)

	graph.end_round_routine()