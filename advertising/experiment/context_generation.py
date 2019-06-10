def disaggregate_context(environment):
	all_disaggregations = environment.get_combinations()

	# TODO: lower bounds

	optimal_disaggregation = all_disaggregations[-1]

	environment.subcampaigns = optimal_disaggregation