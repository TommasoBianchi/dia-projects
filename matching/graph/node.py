class Node:
    def __init__(self, node_class, time_to_stay):
        self.node_class = node_class
        self.time_to_stay = time_to_stay
        self.coin_tossed = False

    def is_critical(self):
        return self.time_to_stay <= 1