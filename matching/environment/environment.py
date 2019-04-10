try:
	# IMPORT FOR PYCHARM USERS
	from matching.distributions.probability_distribution import Bernoulli
except (SystemError, ImportError):
	# IMPORT FOR NON-PYCHARM USERS
	from distributions import Bernoulli

import math

class Environment:
	def __init__(self, classes):
		self.classes = classes

	# Generate new nodes from the new_node_rate_distribution, given the id of the phase we are currently in.
	# The results are returned as a pair (node_class_id, time_to_stay).
	def get_new_nodes(self, phase_id):
		classes = self.classes[phase_id]
		new_nodes = []

		for c in classes:
			new_nodes_amount = c.new_node_rate_distribution.sample()

			# If the new_node_rate_distribution generates fractional values (e.g. it is Gaussian),
			# interpret the fractional part as the probability to have one more node.
			new_nodes_int_amount = math.floor(new_nodes_amount)
			new_nodes_frac_amount = new_nodes_amount - new_nodes_int_amount
			new_nodes_amount = new_nodes_int_amount + Bernoulli(new_nodes_frac_amount).sample()
			new_nodes_amount = max(0, new_nodes_amount) # Make sure new_nodes_amount is never negative
			
			new_nodes += [(c.id, c.time_to_stay_distribution.sample()) for _ in range(new_nodes_amount)]

		return new_nodes

	# Sample a reward for matching a node from class_1 and another one from class_2.
	# Returns a pair (bernoulli_realization, constant_weight).
	def get_reward(class1_id, class2_id, phase_id):
		classes = self.classes[phase_id]
		class1 = [c for c in classes if c.id == class1_id][0]
		edge_data = class1.edge_data[class2_id]
		return (edge_data.weight_distribution.sample(), edge_data.constant_weight)