from matplotlib import pyplot as plt
from agent import State
import os
import glob
import imageio

class World:
    ATTRACTION_SIZE = 50 # Size for plotting
    RED_COUNT = 40*60 # Queue_size for when attractions should be red colored
    FPS = 60
    SAVE_PATH = './save/'

    def __init__(self, agents=[], attractions=[]) -> None:
        self.__agents = agents
        self.__attractions = attractions
        self.history = []
        self.fig, self.ax = plt.subplots()
        plt.draw()

    def clear_exports(self):
        files = glob.glob(self.SAVE_PATH + '*')
        for f in files:
            os.remove(f)

    def get_history(self):
        return self.history
        
    def fill_world(self, agents, attractions):
        self.__agents = agents.copy()
        self.__attractions = attractions.copy()

    def park_empty(self):
        n_out_of_park = 0
        for agent in self.__agents:
            if agent.get_state() == State.OUT_OF_PARK:
                n_out_of_park += 1
        return n_out_of_park == len(self.__agents)

    def save(self, t, export=False):
        self.history.append((self.__agents.copy(), self.__attractions.copy()))
        if export:
            t = format(t, "020b")
            name = f'{t}.png'
            plt.savefig(self.SAVE_PATH+name)

    def build_gif(self):
        frames = []
        files = glob.glob(self.SAVE_PATH + '*')
        for filename in files:
            frames.append(imageio.imread(filename))
        imageio.mimsave("test.gif", frames, format='GIF', fps=30)

    def draw(self, t):
        self.ax.clear()
        self.ax.axis('equal')
        self.draw_agents()
        self.draw_attractions()
        #self.fig.canvas.draw_idle()
        self.ax.set_title("t= " + str(t))
        #plt.pause(1/self.FPS)

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
        
