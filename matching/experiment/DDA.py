class DDA:
    def __init__(self, matching_algorithm):
        self.matching_algorithm = matching_algorithm

    # Check if there is a critical left node ( node that is consuming its TTS ) in the current graph
    def is_there_critical_seller_node(self, graph_nodes):
        left_nodes = [node for node in graph_nodes if node.node_class.is_left]
        return any(node.time_to_stay == 1 for node in left_nodes)

    # Compute the matching with the selected matching algorithm on the passed adjacency matrix
    def perform_matching(self, adjacency_matrix):
        return self.matching_algorithm.compute(adjacency_matrix)
