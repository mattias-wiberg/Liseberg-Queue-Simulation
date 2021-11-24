from agent import Agent
from attraction import Attraction
from world import World
import numpy as np

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
agent1 = Agent((20,20), attractions)
agent2 = Agent((200,1), attractions, 2)
agent3 = Agent((300,150), attractions, 4)
agents = [agent1, agent2, agent3]
world = World(agents, attractions)
world.draw()
for i in range(500):
    for agent in agents:
        agent.update(attractions)
world.draw()

