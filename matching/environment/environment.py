class Environment:
	def __init__(self, classes):
		self.classes = classes

	def get_new_nodes(self, phase_id):
		classes = self.classes[phase_id]
		new_nodes = []

		for c in classes:
			new_nodes_amount = c.new_node_rate_distribution.sample()
			new_nodes += [(c.id, c.time_to_stay_distribution.sample()) for _ in range(new_nodes_amount)]

		return new_nodes

	def get_reward(class1_id, class2_id, phase_id):
		classes = self.classes[phase_id]
		class1 = [c for c in classes if c.id == class1_id][0]
		edge_data = class1.edge_data[class2_id]
		return (edge_data.weight_distribution.sample(), edge_data.constant_weight)