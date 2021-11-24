from agent import Agent, Type
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
        attractions.append(Attraction(name, (x-org_x,y-org_y), ride_size, ride_time, number_of_wagons, delay=10))

attractions = []
load_data('attraction_data.csv', attractions)
agents = []
world = World()
N = 0
for i in range(1000):
    n = np.random.randint(4)+1
    N += n
    agents.append(Agent((np.random.uniform(100, 350), np.random.uniform(200, 600)), attractions, n, type=Type.GREEDY))
    #agents.append(Agent((np.random.uniform(100, 350), np.random.uniform(200, 600)), attractions, world.get_history(), 4, type=Type.GREEDY))

world.fill_world(agents, attractions)
#world.draw()
t = 1
while not world.park_empty():
    for attraction in attractions:
        attraction.advance_queue(t)
        attraction.calc_queue_time(t)
    for agent in agents:
        agent.update()
    world.save()
    if t % 100 == 0:
        print(t)
        #world.draw()
    t += 1
print(t)
print(N)
plt.waitforbuttonpress()
