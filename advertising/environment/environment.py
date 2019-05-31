import subcampaign

class Environment:
    def __init__(self, subcampaigns):
        self.subcampaigns = subcampaigns

    def get_subcampain(self,id):
        if id < len(self.subcampaigns):
            return self.subcampaigns[id]
        return False

    def get_combinations(self):
        result = []
        for subcampaing in self.subcampaigns:
            result.append(subcampaing.disaggregate())
        return result