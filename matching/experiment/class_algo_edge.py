class Class_Algo_Edge:
	def __init__(self, distribution, initial_weight_estimate = 1e9):
		self.distribution = distribution
		self.estimated_weight = initial_weight_estimate
		self.weight_estimation_samples = 0

	def update_estimated_weight(self, sample):
		if self.weight_estimation_samples == 0:
			self.estimated_weight = sample
		else:
			self.estimated_weight += (sample - self.estimated_weight) / self.weight_estimation_samples
		self.weight_estimation_samples += 1