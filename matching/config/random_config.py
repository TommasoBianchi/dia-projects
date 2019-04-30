from random import randint, random

configuration = {
	'phase_data': [
		{
			'duration': 10,
			'left_classes': [
				{
					'new_node_rate_mean': randint(1, 3), 
					'new_node_rate_variance': 2,
					'time_to_stay_min': 2,
					'time_to_stay_max': 5
				},
				{
					'new_node_rate_mean': randint(1, 3), 
					'new_node_rate_variance': 2,
					'time_to_stay_min': 2,
					'time_to_stay_max': 5
				},
				{
					'new_node_rate_mean': randint(1, 3), 
					'new_node_rate_variance': 2,
					'time_to_stay_min': 2,
					'time_to_stay_max': 5
				}
			],
			'right_classes': [
				{
					'new_node_rate_mean': randint(1, 3), 
					'new_node_rate_variance': 2,
					'time_to_stay_min': 2,
					'time_to_stay_max': 5
				},
				{
					'new_node_rate_mean': randint(1, 3), 
					'new_node_rate_variance': 2,
					'time_to_stay_min': 2,
					'time_to_stay_max': 5
				},
				{
					'new_node_rate_mean': randint(1, 3), 
					'new_node_rate_variance': 2,
					'time_to_stay_min': 2,
					'time_to_stay_max': 5
				}
			],
			'edge_data': {
				(0, 0): {
					'mean': random(),
					'weight': randint(1, 10)
				},
				(0, 1): {
					'mean': random(),
					'weight': randint(1, 10)
				},
				(0, 2): {
					'mean': random(),
					'weight': randint(1, 10)
				},
				(1, 0): {
					'mean': random(),
					'weight': randint(1, 10)
				},
				(1, 1): {
					'mean': random(),
					'weight': randint(1, 10)
				},
				(1, 2): {
					'mean': random(),
					'weight': randint(1, 10)
				},
				(2, 0): {
					'mean': random(),
					'weight': randint(1, 10)
				},
				(2, 1): {
					'mean': random(),
					'weight': randint(1, 10)
				},
				(2, 2): {
					'mean': random(),
					'weight': randint(1, 10)
				}
			}
		}
	]
}

def get_configuration():
	return configuration