from agent import Agent
from attraction import Attraction
from world import World
import numpy as np
from matplotlib import pyplot as plt

def load_data(path, attractions):
    data = np.genfromtxt(path, delimiter=',', dtype=("U20",float,float,int,int,int))
    
    R = 6371000 # World radius
    origin = data[0]
    lat = origin[1]
    lon = origin[2]
    org_x = R * np.cos(np.deg2rad(lat)) * np.cos(np.deg2rad(lon))
    org_y = R * np.cos(np.deg2rad(lat)) * np.sin(np.deg2rad(lon))

    for row in data[1:]:
        name = row[0]
        lat = row[1]
        lon = row[2]
        ride_size = row[3]
        ride_time = row[4]
        number_of_wagons = row[5]
        x = R * np.cos(np.deg2rad(lat)) * np.cos(np.deg2rad(lon))
        y = R * np.cos(np.deg2rad(lat)) * np.sin(np.deg2rad(lon))
        attractions.append(Attraction(name, (x-org_x,y-org_y), ride_size, ride_time, number_of_wagons))

attractions = []
load_data('attraction_data.csv', attractions)
agents = []
for i in range(20):
    agents.append(Agent(tuple(np.random.random(2)*500),attractions,np.random.randint(4)+1))
world = World(agents, attractions)
world.draw()
for i in range(400):
    for agent in agents:
        agent.update(attractions)
    if i % 20 == 0:
        world.draw()
plt.waitforbuttonpress()
