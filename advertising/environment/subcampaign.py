
class Subcampaign:

    def __init__(self, classes):
        self.classes = classes

    def sample(self, x):
        val = 0
        for c in self.classes:
            val = val + c.sample(x / len(self.classes))
        return val

    def get_real(self, x):
        val = 0
        for c in self.classes:
            val = val + c.real_function_value(x / len(self.classes))
        return val

    def disaggregate(self):
        combinations = self.__produce_classes_combination()
        subcampaings = []
        for combination in combinations:
            subcampaing = Subcampaign(combination)
            subcampaings.append(subcampaing)
        return subcampaings


    def __produce_classes_combination(self):
        result = []
        for i in range(0, len(self.classes)):
            for c in range(i+1, len(self.classes)):
                if(c < len(self.classes) ):
                    result.append([self.classes[i],self.classes[c]])
        return result