import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

def draw_graph(graph, title = 'Graph'):

	G = nx.Graph()

	node_to_id_dict = {}

	next_id = 0
	for node in graph.nodes:
		G.add_node(next_id)
		node_to_id_dict[node] = next_id
		next_id += 1

	edge_labels = {}

	for edge in graph.edges:
		G.add_edge(node_to_id_dict[edge.node1], node_to_id_dict[edge.node2])
		edge_labels[(node_to_id_dict[edge.node1], node_to_id_dict[edge.node2])] = edge.weight

	plt.title(title)

	left_nodes = [node_to_id_dict[n] for n in graph.nodes if n.node_class.is_left]
	pos = nx.bipartite_layout(G, left_nodes)
	nx.draw(G, pos, with_labels = True)
	nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
	plt.axis('off')
	plt.show()