from copy import deepcopy

class ExperimentMonitor():
	def __init__(self, num_days, day_length, is_on = True):
		self.day_length = day_length
		self.num_days = num_days

		self.is_on = is_on

		self.new_nodes = {}
		self.graph_sizes = {}
		self.all_matchings = {}
		self.all_rewards_by_timestep = {}
		self.all_rewards_by_day = {}
		self.all_rewards_by_phase = {}
		self.all_rewards_by_class = {}
		self.all_best_context_structures = {}

	def new_nodes_added(self, day, round_id, new_nodes):
		if not self.is_on:
			return

		self.new_nodes[(day, round_id)] = deepcopy(new_nodes)

	def graph_size_pre_matching(self, day, round_id, node_size, edge_size):
		if not self.is_on:
			return
			
		self.graph_sizes[(day, round_id)] = {'pre_matching': (node_size, edge_size)}

	def graph_size_post_matching(self, day, round_id, node_size, edge_size):
		if not self.is_on:
			return
			
		self.graph_sizes[(day, round_id)]['post_matching'] = (node_size, edge_size)

	def matching_performed(self, day, round_id, matching_edges, full_matching_edges):
		if not self.is_on:
			return
			
		self.all_matchings[(day, round_id)] = {
			'matching_edges': [(e.node1.node_class.id, e.node2.node_class.id, e.weight) for e in matching_edges],
			'full_matching_edges': [(e.node1.node_class.id, e.node2.node_class.id, e.weight) for e in full_matching_edges]
		}

	def reward_collected(self, day, round_id, phase_id, class1_id, class2_id, reward_realization, reward_weight):
		if not self.is_on:
			return

		reward_data = {'day': day, 'round_id': round_id, 'phase_id': phase_id,
					   'class1_id':class1_id, 'class2_id': class2_id, 
					   'reward_realization': reward_realization, 'reward_weight': reward_weight}

		if (day, round_id) not in self.all_rewards_by_timestep:
			self.all_rewards_by_timestep[(day, round_id)] = []
		self.all_rewards_by_timestep[(day, round_id)].append(reward_data)
			
		if day not in self.all_rewards_by_day:
			self.all_rewards_by_day[day] = []
		self.all_rewards_by_day[day].append(reward_data)

		if phase_id not in self.all_rewards_by_phase:
			self.all_rewards_by_phase[phase_id] = []
		self.all_rewards_by_phase[phase_id].append(reward_data)

		if (class1_id, class2_id) not in self.all_rewards_by_class:
			self.all_rewards_by_class[(class1_id, class2_id)] = []
		self.all_rewards_by_class[(class1_id, class2_id)].append(reward_data)

	def context_generation_performed(self, day, best_context_structure):
		if not self.is_on:
			return
			
		return

	def get_matching_sizes(self):			
		matching_size_per_timestep = []
		matching_size_per_day = []

		for day in range(self.num_days):
			matches_this_day = 0
			for round_id in range(self.day_length):
				if (day, round_id) in self.all_matchings:
					num_matchings = len(self.all_matchings[(day, round_id)])
					matching_size_per_timestep.append(num_matchings)
					matches_this_day += num_matchings
				else:
					matching_size_per_timestep.append(0)
			matching_size_per_day.append(matches_this_day)

		return {'per_timestamp': matching_size_per_timestep, 'per_day': matching_size_per_day}

	def get_graph_sizes(self):			
		graph_size_per_timestamp_pre = []
		graph_size_per_timestamp_post = []
		graph_size_per_day_pre = []
		graph_size_per_day_post = []

		for day in range(self.num_days):
			size_pre_this_day = 0
			size_post_this_day = 0
			for round_id in range(self.day_length):
				if (day, round_id) in self.graph_sizes:
					size = self.graph_sizes[(day, round_id)]
					graph_size_per_timestamp_pre.append(size['pre_matching'])
					size_pre_this_day += size['pre_matching'][1] # Size in number of edges
					graph_size_per_timestamp_post.append(size['post_matching'])
					size_post_this_day += size['post_matching'][1]
			graph_size_per_day_pre.append(size_pre_this_day / self.day_length)
			graph_size_per_day_post.append(size_post_this_day / self.day_length)

		return {'pre_matching': {'per_timestamp': graph_size_per_timestamp_pre, 'per_day': graph_size_per_day_pre},
				'post_matching': {'per_timestamp': graph_size_per_timestamp_post, 'per_day': graph_size_per_day_post}}

	def get_rewards_per_arm(self):			
		all_classes = list(self.all_rewards_by_class.keys())

		rewards_per_arm_per_day = {c: [] for c in all_classes}
		rewards_per_arm_per_timestep = {c: [] for c in all_classes} # TODO: implement

		for day in range(self.num_days):
			if day in self.all_rewards_by_day:
				reward_per_class = {c: 0 for c in all_classes}
				for reward_data in self.all_rewards_by_day[day]:
					class_pair = (reward_data['class1_id'], reward_data['class2_id'])
					reward_per_class[class_pair] += reward_data['reward_realization'] * reward_data['reward_weight']
				for (c, r) in reward_per_class.items():
					rewards_per_arm_per_day[c].append(r)

		return {'per_timestamp': rewards_per_arm_per_timestep, 'per_day': rewards_per_arm_per_day}

	def get_number_of_arm_pulls(self):			
		all_classes = list(self.all_rewards_by_class.keys())

		pulls_per_arm_per_day = {c: [] for c in all_classes}
		pulls_per_arm_per_timestep = {c: [] for c in all_classes} # TODO: implement

		for day in range(self.num_days):
			if day in self.all_rewards_by_day:
				pulls_per_class = {c: 0 for c in all_classes}
				for reward_data in self.all_rewards_by_day[day]:
					class_pair = (reward_data['class1_id'], reward_data['class2_id'])
					pulls_per_class[class_pair] += 1
				for (c, r) in pulls_per_class.items():
					pulls_per_arm_per_day[c].append(r)

		return {'per_timestamp': pulls_per_arm_per_timestep, 'per_day': pulls_per_arm_per_day}				