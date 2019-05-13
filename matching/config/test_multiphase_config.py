configuration = { 
					'phase_data': [
						###########
						# PHASE 1
						###########
						{
							'duration': 4,
							'left_classes': [
								{
									'new_node_rate_mean': 0, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								},
								{
									'new_node_rate_mean': 0, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								}
							],
							'right_classes': [
								{
									'new_node_rate_mean': 0, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								},
								{
									'new_node_rate_mean': 0, 
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
								(1, 0): {
									'mean': 0.4,
									'weight': 4
								},
								(1, 1): {
									'mean': 0.5,
									'weight': 5
								}
							}
						},
						###########
						# PHASE 2
						###########
						{
							'duration': 4,
							'left_classes': [
								{
									'new_node_rate_mean': 0, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								},
								{
									'new_node_rate_mean': 0, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								}
							],
							'right_classes': [
								{
									'new_node_rate_mean': 0, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								},
								{
									'new_node_rate_mean': 0, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								}
							],
							'edge_data': {
								(0, 0): {
									'mean': 0.35,
									'weight': 7
								},
								(0, 1): {
									'mean': 0.3,
									'weight': 8
								},
								(1, 0): {
									'mean': 0.4,
									'weight': 5
								},
								(1, 1): {
									'mean': 0.2,
									'weight': 3
								}
							}
						},
						###########
						# PHASE 3
						###########
						{
							'duration': 4,
							'left_classes': [
								{
									'new_node_rate_mean': 0, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								},
								{
									'new_node_rate_mean': 0, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								}
							],
							'right_classes': [
								{
									'new_node_rate_mean': 0, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								},
								{
									'new_node_rate_mean': 0, 
									'new_node_rate_variance': 1,
									'time_to_stay_min': 2,
									'time_to_stay_max': 5
								}
							],
							'edge_data': {
								(0, 0): {
									'mean': 0.1,
									'weight': 12
								},
								(0, 1): {
									'mean': 0.25,
									'weight': 6
								},
								(1, 0): {
									'mean': 0.7,
									'weight': 4
								},
								(1, 1): {
									'mean': 0.001,
									'weight': 100
								}
							}
						}
					]
				}

def get_configuration():
	return configuration