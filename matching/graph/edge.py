class Edge:
    def __init__(self, node1, node2):
    	# Always have the node with the smallest class_id as the first one

        self.node1 = min([node1, node2], key = lambda n: n.node_class.id)
        self.node2 = max([node1, node2], key = lambda n: n.node_class.id)

        self.last_weight_estimate_sample_size = -1

    # Update the estimated weight of the edge.
    def update_weight(self, force_update = False):
        edge_data = self.node1.node_class.edge_data[self.node2.node_class.id]

        # Update the estimated weight only if we have more data on which to estimate
        # This is especially important for TS, as it avoids constantly taking new samples
        # from the Beta distribution that will make the like of DDA much more complicated
        if force_update or self.last_weight_estimate_sample_size != edge_data.weight_estimation_samples:
        	self.weight = edge_data.distribution.sample() * edge_data.estimated_weight
        	self.last_weight_estimate_sample_size = edge_data.weight_estimation_samples