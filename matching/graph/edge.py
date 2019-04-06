class Edge:
	def __init__(self, node1, node2):
		self.node1 = node1
		self.node2 = node2

	def update_weight(self):
		edge_data = self.node1.node_class.edge_data[self.node2.node_class.id]
		self.weight = edge_data.distribution.sample() * edge_data.estimated_weight