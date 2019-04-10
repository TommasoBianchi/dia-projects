# IMPORT FOR PYCHARM USERS

from matching.graph.node import Node
from matching.graph.edge import Edge

# IMPORT FOR NON-PYCHARM USERS

# from graph.node import Node
# from graph.edge import Edge

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node_class, time_to_stay):
        node = Node(node_class, time_to_stay)

        for other_node in self.nodes:
            if other_node.node_class.is_left != node.node_class.is_left:
                edge = Edge(node, other_node)
                self.edges.append(edge)

        self.nodes.append(node)

        return node

    def update_weights(self):
        for edge in self.edges:
            edge.update_weight()

    def remove_node(self, node):
        self.nodes.remove(node)
        self.edges = [e for e in self.edges if (e.node1 != node and e.node2 != node)]

    def end_round_routine(self):
        for node in self.nodes:
            if node.time_to_stay > 1:
                node.time_to_stay -= 1
            else:
                self.remove_node(node)
