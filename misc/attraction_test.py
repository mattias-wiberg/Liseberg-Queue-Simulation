from agent import Agent
from attraction import Attraction
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

agent1 = Agent((1,1), attractions, 2)
agent2 = Agent((1,1), attractions, 4)
agent3 = Agent((1,1), attractions, 1)
agent4 = Agent((1,1), attractions, 2)
agent5 = Agent((1,1), attractions, 4)
agent6 = Agent((1,1), attractions, 2)


attraction1 = Attraction(name="flumeride", attraction_coeff=1.0, wagon_size=4, wagon_ride_time=210, n_wagons=28, position=(1,1), delay=0, extrapolate_pts=5)

attraction1.add_to_queue(agent1)
attraction1.add_to_queue(agent2)
attraction1.add_to_queue(agent3)
attraction1.add_to_queue(agent4)
attraction1.add_to_queue(agent5)
attraction1.add_to_queue(agent6)

global_time = 1
queue_size = attraction1.get_queue_size()
while True:
    attraction1.advance_queue(global_time)
    attraction1.calc_queue_time(global_time)
    print(f'[{global_time}] Queue time: {attraction1.get_queue_time()}')
    print(f'[{global_time}] Expected queue time at {global_time+5} : {attraction1.get_extrapolated_queue_time(global_time+5)}')
    queue_size = attraction1.get_queue_size()
    if queue_size == 0:
        break
        global_time += 1
    else:
        global_time += 1


print(f"Queue empty at {global_time}")

