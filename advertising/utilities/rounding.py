def round_to_nearest_feasible_superarm(super_arm, arms):
	for i in range(len(super_arm)):
		if super_arm[i][1] in arms:
			continue

		lower_arm = list(filter(lambda a: a < super_arm[i][1], arms))[-1]
		super_arm[i] = (super_arm[i][0], lower_arm)

	super_arm[-1] = (super_arm[-1][0], arms[-1] - sum(map(lambda x: x[1], super_arm[:-1])))
	return super_arm