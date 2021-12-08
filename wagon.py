class Wagon:
    def __init__(self):
        self.agents_in_wagon = []

    def get_agents(self):
        return self.agents_in_wagon
    
    def clear(self):
        temp = self.agents_in_wagon
        self.agents_in_wagon = []
        return temp

    def add_agent(self, agent):
        self.agents_in_wagon.append(agent)
