class Edge:
    def __init__(self, node1, node2):
    	# Always have the node with the smallest class_id as the first one

        self.node1 = min([node1, node2], key = lambda n: n.node_class.id)
        self.node2 = max([node1, node2], key = lambda n: n.node_class.id)

    # Update the estimated weight of the edge.
    def update_weight(self):
        edge_data = self.node1.node_class.edge_data[self.node2.node_class.id]
        self.weight = edge_data.distribution.sample() * edge_data.estimated_weight
