class Class_Algo:
	def __init__(self, id, is_left):
		self.id = id
		self.is_left = is_left
		self.edge_data = {}

	def set_edge_data(self, other_class, edge_data):
		self.edge_data[other_class.id] = edge_data