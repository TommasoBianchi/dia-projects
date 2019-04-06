from graph import Graph
from experiment.class_algo import Class_Algo
from experiment.class_edge import Class_Edge
from distributions import Beta
from utilities.drawing import draw_graph
from random import randint

graph = Graph()

left_classes_ids = [1, 2]
right_classes_ids = [3]

classes = [Class_Algo(id, True) for id in left_classes_ids] + [Class_Algo(id, False) for id in right_classes_ids]

for i in left_classes_ids:
	for j in right_classes_ids:
		class_edge = Class_Edge(Beta())
		l_class = [c for c in classes if c.id == i][0]
		r_class = [c for c in classes if c.id == j][0]
		l_class.set_edge_data(r_class, class_edge)
		r_class.set_edge_data(l_class, class_edge)

for _ in range(10):
	graph.add_node(classes[randint(0, len(classes)-1)], randint(1, 10))

graph.update_weights()

draw_graph(graph)