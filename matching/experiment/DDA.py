import random


class DDA:
    def __init__(self, matching_algorithm):
        self.matching_algorithm = matching_algorithm

    # Check if there is a critical left node ( node that is consuming its TTS ) in the current graph
    def is_there_critical_seller_node(self, graph_nodes):
        return any(node.time_to_stay == 1 for node in graph_nodes)

    # Toss a coin: if the result is 1, the matching is allowed and assigned to the solution
    def toss_coin(self, final_matching, edge):
        flip = random.randint(0, 1)
        if flip == 1:
            final_matching.append(edge)

        else:
            edge.node1.coin_tossed = True
            edge.node2.coin_tossed = True

        return final_matching, edge

    # Return the list of critical nodes of the edge
    def critical_nodes(self, edge):
        critical_nodes = []
        if edge.node1.is_critical:
            critical_nodes.append(edge.node1)

        if edge.node2.is_critical:
            critical_nodes.append(edge.node2)

        return len(critical_nodes)

    # Return true if the edge contains critical nodes, False otherwise
    def is_edge_critical(self, edge):
        if edge.node1.is_critical() or edge.node1.is_critical():
            return True
        else:
            return False


    # Compute the matching with the selected matching algorithm on the passed adjacency matrix. It returns the edges
    # of the final assignment and the graph with the nodes updated with the coin toss resulting labels
    def perform_matching(self, graph):
        adjacency_matrix = graph.get_adjacency_matrix()
        _, matching_assignment = self.matching_algorithm.compute(adjacency_matrix)

        # First node in the edge is the left ( seller ) one and the second is the right one ( buyer )
        matching_edges = graph.get_edges_from_matching(matching_assignment)

        final_matching_edges = []
        updated_edges = []
        for edge in matching_edges:
            if self.is_edge_critical(edge):
                if self.critical_nodes(edge) == 2:
                    final_matching_edges.append(edge)

                else:
                    final_matching_edges, edge = self.toss_coin(final_matching_edges, edge)
            updated_edges.append(edge)

        graph.edges = updated_edges
        return final_matching_edges, graph




