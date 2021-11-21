from matplotlib import pyplot

class World:
    def __init__(self, agents, attractions) -> None:
        self.__agents = agents
        self.__attractions = attractions
        
    def draw(self):
        self.draw_agents()
        self.draw_attractions()
        pyplot.show()

    def draw_agents(self):
        for agent in self.__agents:
            position = agent.get_position()
            pyplot.scatter(position[0], position[1], color='g')
        

    def draw_attractions(self):
        for attration in self.__attractions:
            position = attration.get_position()
            pyplot.scatter(position[0], position[1], c=[[1.0, 0, 0]])
        
