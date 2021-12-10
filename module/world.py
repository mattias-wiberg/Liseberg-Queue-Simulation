from typing import List
from matplotlib import pyplot as plt
from agent import State
import os
import glob
import imageio
import numpy as np
from agent import Agent
from spawn import Spawn
from attraction import Attraction
import pickle


class World:
    ATTRACTION_SIZE = 50  # Size for plotting
    RED_COUNT = 40*60  # Queue_size for when attractions should be red colored
    FPS = 60
    SAVE_PATH = './gif_save/'

    def __init__(self, attractions=None, spawns=None, agents=None) -> None:
        if attractions is None:
            self.attractions = []
        if spawns is None:
            self.spawns = []
        if agents is None:
            self.agents = []
        self.history = []
        self.n_agents = 0
        self.fig, self.ax = plt.subplots()
        plt.draw()

    def load_park(self, path, delay, extrapolate_pts) -> List:
        data = np.genfromtxt(path, delimiter=',', dtype=(
            "U20", "U20", float, float, int, int, int))
        R = 6371000  # World radius
        origin = data[0]
        lat = origin[2]
        lon = origin[3]
        org_x = R * np.cos(np.deg2rad(lat)) * np.cos(np.deg2rad(lon))
        org_y = R * np.cos(np.deg2rad(lat)) * np.sin(np.deg2rad(lon))

        for row in data:  # Load spawn
            type = row[0]
            name = row[1]
            lat = row[2]
            lon = row[3]
            ride_size = row[4]
            ride_time = row[5]
            number_of_wagons = row[6]
            x = R * np.cos(np.deg2rad(lat)) * np.cos(np.deg2rad(lon))
            y = R * np.cos(np.deg2rad(lat)) * np.sin(np.deg2rad(lon))
            # Shift and rotate -90deg
            x, y = np.array([[0, 1], [-1, 0]]).dot([x-org_x, y-org_y])

            if type == "SPAWN":
                self.spawns.append(Spawn(name, (x, y)))
            elif type == "ATTRACTION":
                self.attractions.append(Attraction(
                    name, (x, y), ride_size, ride_time, number_of_wagons, delay=delay, extrapolate_pts=extrapolate_pts))
            else:
                print("Error: Unidentified type ("+type+") in " +
                      path+" skipping row.")

    def spawn_agent(self, type, commit_prob, queue_prob, view_range, visit_window) -> Agent:
        n = np.random.randint(1, 5)
        self.n_agents += n
        self.agents.append(Agent(np.random.choice(self.spawns).position, self.attractions,
                           queue_prob, commit_prob, view_range, n, type, visit_window))
        return self.agents[-1]

    def populate(self, n_agents, _type, _commit_prob) -> List:
        while self.n_agents < n_agents:
            self.spawn_agent(_type, _commit_prob)
        return self.agents

    def park_empty(self):
        n_out_of_park = 0
        for agent in self.agents:
            if agent.get_state() == State.OUT_OF_PARK:
                n_out_of_park += 1
        return n_out_of_park == len(self.agents)

    def add_to_history(self):
        agents_copy = list(
            map(lambda agent: agent.shallow_copy(), self.agents))
        self.history.append((agents_copy, list(
            map(lambda attraction: attraction.get_shallow_copy(), self.attractions))))

    def dump(self, logs_path, name):
        with open(logs_path+"/"+name+".p", "wb") as f:
            pickle.dump(self.history, f)

    def clear_pngs(self, path=SAVE_PATH):
        files = glob.glob(path + '*')
        for f in files:
            os.remove(f)

    def save_png(self, t):
        t = format(t, "020b")
        name = f'{t}.png'
        plt.savefig(self.SAVE_PATH+name)

    def build_gif(self, name="new_gif.gif", path=SAVE_PATH):
        frames = []
        files = glob.glob(path + '*')
        for filename in files:
            frames.append(imageio.imread(filename))
        imageio.mimsave(name, frames, format='GIF', fps=30)

    def draw(self, t, draw_continuously=True):
        self.ax.clear()
        self.ax.axis('equal')
        self.draw_agents()
        self.draw_attractions()
        self.draw_spawns()
        self.ax.set_title("t= " + str(t))

        if draw_continuously:
            self.fig.canvas.draw_idle()
            plt.pause(1/self.FPS)

    def draw_agents(self):
        for agent in self.agents:
            if agent.get_state() == State.IN_PARK:
                position = agent.get_position()
                self.ax.scatter(
                    position[0], position[1], s=self.ATTRACTION_SIZE*agent.get_group_size()/4, color='b')

    def draw_spawns(self):
        for spawn in self.spawns:
            position = spawn.position
            self.ax.scatter(position[0], position[1], s=self.ATTRACTION_SIZE, c=[
                            [170/250, 0, 1]], marker='^')

    def draw_attractions(self):
        for attraction in self.attractions:
            position = attraction.get_position()
            queue_time = attraction.get_queue_time()
            ratio = min(1, queue_time/self.RED_COUNT)
            # c = [R, G, B]
            self.ax.scatter(position[0], position[1], s=self.ATTRACTION_SIZE, c=[
                            [ratio, 1-ratio, 0]], marker='s')

    def get_history(self):
        return self.history
