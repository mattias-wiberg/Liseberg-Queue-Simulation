class Wagon:
    def __init__(self):
        self.__agents_in_wagon = []

    def get_agents(self):
        return self.__agents_in_wagon
    
    def clear(self):
        temp = self.__agents_in_wagon
        self.__agents_in_wagon = []
        return temp

    def add_agent(self, agent):
        self.__agents_in_wagon.append(agent)
