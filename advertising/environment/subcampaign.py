from utilities.partitioning import partition

class Subcampaign:

    def __init__(self, classes):
        self.classes = classes

    def sample(self, x):
        return tuple([c.sample(x / len(self.classes)) for c in self.classes])

    def get_real(self, x):
        val = 0
        for c in self.classes:
            val = val + c.real_function_value(x / len(self.classes))
        return val

    def get_classes_ids(self):
        return tuple([c.id for c in self.classes])

    def disaggregate(self):
        class_indices = list(range(len(self.classes)))
        all_partitions = partition(class_indices)
        subcampaigns = []
        for p in all_partitions:
            p_subcampaigns = []
            for indices in p:
                p_subcampaigns.append(Subcampaign([self.classes[i].copy() for i in indices]))
            subcampaigns.append(p_subcampaigns)
        return subcampaigns

    def get_samples(self):
        samples = []
        for t in range(len(self.classes[0].samples)):
            iteration_samples = [c.samples[t] for c in self.classes]
            samples.append((sum([x[0] for x in iteration_samples]), sum([x[1] for x in iteration_samples])))
        return samples

    def copy(self):
        return Subcampaign([c.copy() for c in self.classes])