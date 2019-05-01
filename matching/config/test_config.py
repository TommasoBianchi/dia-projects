configuration = { 
					'phase_data': [
						{
							'duration': 10,
							'left_classes': [
								{
									'new_node_rate_mean': 1, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								},
								{
									'new_node_rate_mean': 1, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								},
								{
									'new_node_rate_mean': 1, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								}
							],
							'right_classes': [
								{
									'new_node_rate_mean': 1, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								},
								{
									'new_node_rate_mean': 1, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								},
								{
									'new_node_rate_mean': 1, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								}
							],
							'edge_data': {
								(0, 0): {
									'mean': 0.2,
									'weight': 7
								},
								(0, 1): {
									'mean': 0.35,
									'weight': 5
								},
								(0, 2): {
									'mean': 0.8,
									'weight': 2
								},
								(1, 0): {
									'mean': 0.4,
									'weight': 4
								},
								(1, 1): {
									'mean': 0.5,
									'weight': 5
								},
								(1, 2): {
									'mean': 0.5,
									'weight': 3.5
								},
								(2, 0): {
									'mean': 0.3,
									'weight': 6
								},
								(2, 1): {
									'mean': 0.9,
									'weight': 1
								},
								(2, 2): {
									'mean': 0.1,
									'weight': 12
								}
							}
						}
					]
				}

def get_configuration():
	return configuration