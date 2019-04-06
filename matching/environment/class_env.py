class Class_Env:
	def __init__(self, id, is_left, new_node_rate_distribution, time_to_stay_distribution):
		self.id = id
		self.is_left = is_left
		self.new_node_rate_distribution = new_node_rate_distribution
		self.time_to_stay_distribution = time_to_stay_distribution
		self.edge_data = {}

	def set_edge_data(self, other_class, edge_data):
		self.edge_data[other_class.id] = edge_data