try:
	# IMPORT FOR PYCHARM USERS
	from matching.environment.environment import Environment
except (SystemError, ImportError):
	# IMPORT FOR NON-PYCHARM USERS
	from environment.environment import Environment

from copy import deepcopy

class RestorableEnvironment(Environment):
	def __init__(self, classes):
		Environment.__init__(self, classes)

		# Store all the stochastic data to be able to replay them deterministically when requested
		self.restored_new_nodes = {}
		self.saved_new_nodes = {}
		self.restored_rewards = {}
		self.saved_rewards = {}

	def get_new_nodes(self, phase_id):
		if phase_id in self.restored_new_nodes and len(self.restored_new_nodes[phase_id]) > 0:
			new_nodes = self.restored_new_nodes[phase_id].pop(0)
		else:
			new_nodes = Environment.get_new_nodes(self, phase_id)

		# Save generated new nodes
		if phase_id not in self.saved_new_nodes:
			self.saved_new_nodes[phase_id] = []
		self.saved_new_nodes[phase_id].append(new_nodes)

		return new_nodes

	def get_reward(self, class1_id, class2_id, phase_id):
		# To avoid problems with requesting a reward for classes (1, 3) and/or for classes
		# (3, 1), we store old data keeping class_ids in order
		key = (phase_id, min(class1_id, class2_id), max(class1_id, class2_id))

		if key in self.restored_rewards and len(self.restored_rewards[key]) > 0:
			reward = self.restored_rewards[key].pop(0)
		else:
			reward = Environment.get_reward(self, class1_id, class2_id, phase_id)

		# Save generated rewards
		if key not in self.saved_rewards:
			self.saved_rewards[key] = []
		self.saved_rewards[key].append(reward)

		return reward

	def restore(self):
		# Save all the remaining restored stuff (if any)
		for (k, v) in self.restored_new_nodes.items():
			if k not in self.saved_new_nodes:
				self.saved_new_nodes[k] = []
			self.saved_new_nodes[k] += v

		for (k, v) in self.restored_rewards.items():
			if k not in self.saved_rewards:
				self.saved_rewards[k] = []
			self.saved_rewards[k] += v

		# Restore saved data and cleanup the space for saving them
		self.restored_new_nodes = self.saved_new_nodes
		self.saved_new_nodes = {}
		self.restored_rewards = self.saved_rewards
		self.saved_rewards = {}