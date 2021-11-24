from matplotlib import pyplot as plt
from agent import State

class World:
    ATTRACTION_SIZE = 50 # Size for plotting
    RED_COUNT = 180 # Queue_size for when attractions should be red colored
    FPS = 1

    def __init__(self, agents, attractions) -> None:
        self.__agents = agents
        self.__attractions = attractions
        self.history = []
        self.fig, self.ax = plt.subplots()
        plt.draw()

    def get_history(self):
        return self.history
        
    def save(self):
        self.history.append((self.agents.copy(), self.attractions.copy()))

    def draw(self):
        self.ax.clear()
        #self.ax.set_xlim(100,400)
        #self.ax.set_ylim(200,600)
        self.draw_agents()
        self.draw_attractions()
        self.fig.canvas.draw_idle()
        plt.pause(1/self.FPS)
        # TODO https://stackoverflow.com/questions/42722691/python-matplotlib-update-scatter-plot-from-a-function

    def draw_agents(self):
        for agent in self.__agents:
            if agent.get_state() == State.IN_PARK:
                position = agent.get_position()
                self.ax.scatter(position[0], position[1], s=self.ATTRACTION_SIZE*agent.get_group_size()/4, color='b')
        

    def draw_attractions(self):
        for attraction in self.__attractions:
            position = attraction.get_position()
            queue_time = attraction.get_queue_time()
            ratio = min(1, queue_time/self.RED_COUNT)
            # c = [R, G, B]
            self.ax.scatter(position[0], position[1], s=self.ATTRACTION_SIZE, c=[[ratio, 1-ratio, 0]], marker='s')
        
