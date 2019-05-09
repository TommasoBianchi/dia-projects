def generate_context_structures(day_length = 24, min_phase_length = 1, min_num_phases = 1):
	max_num_phases = int(day_length / min_phase_length)
	max_phase_length = int(day_length / min_num_phases)

	def add_single_phase(context_structures, day_length, min_phase_length, max_phase_length):
		expanded_context_structures = []

		for context in context_structures:
			remaining_day_length = day_length - sum(context)

			for phase_length in range(min_phase_length, remaining_day_length+1):
				expanded_context_structures.append(context + [ phase_length ])

		return expanded_context_structures

	all_context_structures = []

	for n_phases in range(min_num_phases, max_num_phases+1):
		context_structures = [[]]
		for _ in range(n_phases):
			context_structures = add_single_phase(context_structures, day_length,
												  min_phase_length, max_phase_length)

		context_structures = [cs for cs in context_structures if sum(cs) == day_length]

		all_context_structures += context_structures

	return all_context_structures