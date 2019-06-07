print("Job Matching Service")

"""
    This is a Job Matching Service. The Environment considered is composed by 6 classes: three of them are constituted 
    by group of candidates in the IT with distinct skills looking for their dream job, and the other half is composed by
    companies with different goals and aiming to hire the perfect candidate. 
    
    The candidates classes are: Machine Learning Engineers, Software Engineers and Front End Developers. 
    Instead, the companies categories taken into account are specialize respectively in: Video Game Development,
    implementation of Mobile Applications and Recommender Systems design.
    
    The two set of three classes represent the two sides of the matching problem that our project aim to solve.
    The interest of the different groups of candidates for a certain category of companies and, vice-versa, the 
    relevance that a category of companies gives to a candidate with a particular skill change across the four phases. 
 """
configuration = {

    # LEFT:
    #
    # 0: Machine Learning Engineers
    # 1: Software Engineers
    # 2: Front End Developers
    #
    # RIGHT:
    #
    # 0: Video Game Companies
    # 1: Mobile Application Companies
    # 2: Recommender System Companies
    #
    #

    'phase_data': [
        ###########
        # PHASE 1
        ###########
        {
            'duration': 3,
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
                    'weight': 7
                },
                (0, 1): {
                    'mean': 0.4,
                    'weight': 4
                },
                (0, 2): {
                    'mean': 0.6,
                    'weight': 15
                },
                (1, 0): {
                    'mean': 0.3,
                    'weight': 18
                },
                (1, 1): {
                    'mean': 0.9,
                    'weight': 13
                },
                (1, 2): {
                    'mean': 0.5,
                    'weight': 8
                },
                (2, 0): {
                    'mean': 0.6,
                    'weight': 11
                },
                (2, 1): {
                    'mean': 0.6,
                    'weight': 9
                },
                (2, 2): {
                    'mean': 0.2,
                    'weight': 5
                }
            }
        },
        ###########
        # PHASE 2
        ###########
        {
            'duration': 3,
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
                    'mean': 0.3,
                    'weight': 8
                },
                (0, 1): {
                    'mean': 0.2,
                    'weight': 7
                },
                (0, 2): {
                    'mean': 0.9,
                    'weight': 18
                },
                (1, 0): {
                    'mean': 0.8,
                    'weight': 16
                },
                (1, 1): {
                    'mean': 0.7,
                    'weight': 10
                },
                (1, 2): {
                    'mean': 0.2,
                    'weight': 6
                },
                (2, 0): {
                    'mean': 0.5,
                    'weight': 12
                },
                (2, 1): {
                    'mean': 0.8,
                    'weight': 15
                },
                (2, 2): {
                    'mean': 0.35,
                    'weight': 3
                }
            }
        },
        ###########
        # PHASE 3
        ###########
        {
            'duration': 3,
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
                    'mean': 0.6,
                    'weight': 10
                },
                (0, 1): {
                    'mean': 0.8,
                    'weight': 17
                },
                (0, 2): {
                    'mean': 0.2,
                    'weight': 9
                },
                (1, 0): {
                    'mean': 0.83,
                    'weight': 3
                },
                (1, 1): {
                    'mean': 0.3,
                    'weight': 14
                },
                (1, 2): {
                    'mean': 0.65,
                    'weight': 12
                },
                (2, 0): {
                    'mean': 0.5,
                    'weight': 8
                },
                (2, 1): {
                    'mean': 0.1,
                    'weight': 3
                },
                (2, 2): {
                    'mean': 0.8,
                    'weight': 7
                }
            }
        },
        ###########
        # PHASE 4
        ###########
        {
            'duration': 3,
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
                    'mean': 0.3,
                    'weight': 8
                },
                (0, 1): {
                    'mean': 0.1,
                    'weight': 2
                },
                (0, 2): {
                    'mean': 0.95,
                    'weight': 20
                },
                (1, 0): {
                    'mean': 0.7,
                    'weight': 5
                },
                (1, 1): {
                    'mean': 0.3,
                    'weight': 5
                },
                (1, 2): {
                    'mean': 0.2,
                    'weight': 13
                },
                (2, 0): {
                    'mean': 0.9,
                    'weight': 17
                },
                (2, 1): {
                    'mean': 0.2,
                    'weight': 3
                },
                (2, 2): {
                    'mean': 0.8,
                    'weight': 15
                }
            }
        }
    ]
}


def get_configuration():
    return configuration
