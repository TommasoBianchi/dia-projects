class Class_Algo_Edge:
	def __init__(self, distribution, initial_weight_estimate = 1e9):
		self.distribution = distribution
		self.estimated_weight = initial_weight_estimate
		self.weight_estimation_samples = 0