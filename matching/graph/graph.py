try:
    # IMPORT FOR PYCHARM USERS

    from matching.graph.node import Node
    from matching.graph.edge import Edge
except (SystemError, ImportError):
    # IMPORT FOR NON-PYCHARM USERS

    from graph.node import Node
    from graph.edge import Edge

import numpy as np

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    # Add a new node to the graph that belongs to a given node_class and with a given time_to_stay (i.e. rounds to stay in the graph).
    # This method automatically adds edges between this node and any other node on the other side of the graph (it is supposed
    # to be a bipartite graph).
    def add_node(self, node_class, time_to_stay):
        node = Node(node_class, time_to_stay)

        for other_node in self.nodes:
            if other_node.node_class.is_left != node.node_class.is_left:
                edge = Edge(node, other_node)
                self.edges.append(edge)

        self.nodes.append(node)

        return node

    # Update the estimated weights on all edges of the graph.
    def update_weights(self, force_update = False):
        for edge in self.edges:
            edge.update_weight(force_update)

    # Remove a given node (and all of its incident edges) from the graph.
    def remove_node(self, node):
        self.nodes.remove(node)
        self.edges = [e for e in self.edges if (e.node1 != node and e.node2 != node)]

    # Perform the final phase of a round, that is reduce by one the time_to_stay of each node and remove
    # nodes that have finished their life.
    def end_round_routine(self):
        for node in self.nodes:
            if node.time_to_stay > 1:
                node.time_to_stay -= 1
            else:
                self.remove_node(node)

    # Build the adjacency matrix of this graph as a numpy matrix (the graph is assumed to be bipartite).
    def get_adjacency_matrix(self):
        left_nodes = [n for n in self.nodes if n.node_class.is_left]
        right_nodes = [n for n in self.nodes if not n.node_class.is_left]
        matrix = np.zeros(shape = (len(left_nodes), len(right_nodes)))

        for edge in self.edges:
            if edge.node1.node_class.is_left:
                l_node = edge.node1
                r_node = edge.node2
            else:
                l_node = edge.node2
                r_node = edge.node1
            l_node_index = left_nodes.index(l_node)
            r_node_index = right_nodes.index(r_node)
            matrix[l_node_index, r_node_index] = edge.weight

        return matrix

    # Transform a matching matrix (composed of 0/1 values) into a list of matched edges.
    def get_edges_from_matching(self, matching_matrix):
        edges = []

        left_nodes = [n for n in self.nodes if n.node_class.is_left]
        right_nodes = [n for n in self.nodes if not n.node_class.is_left]

        for edge in self.edges:
            if edge.node1.node_class.is_left:
                l_node = edge.node1
                r_node = edge.node2
            else:
                l_node = edge.node2
                r_node = edge.node1
            l_node_index = left_nodes.index(l_node)
            r_node_index = right_nodes.index(r_node)
            if matching_matrix[l_node_index, r_node_index] == 1:
                edges.append(edge)

        return edges