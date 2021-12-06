import random
from agent import Agent, Type
from attraction import Attraction
from world import World
import numpy as np
from matplotlib import pyplot as plt
import cProfile
from pstats import Stats, SortKey
np.random.seed(10)
random.seed(10)

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
        x,y = np.array([[0, 1],[-1, 0]]).dot([x-org_x,y-org_y]) # Shift and rotate -90deg
        attractions.append(Attraction(name, (x,y), ride_size, ride_time, number_of_wagons, delay=0, extrapolate_pts=2))
        
def run_model():
    attractions = []
    load_data('attraction_data.csv', attractions)
    agents = []
    world = World()
    N = 0
    for i in range(1000):
        n = np.random.randint(4)+1
        N += n
        agents.append(Agent((np.random.uniform(0, 400), np.random.uniform(0, -250)), attractions, n, type=Type.NAIVE))
        #agents.append(Agent((np.random.uniform(100, 350), np.random.uniform(200, 600)), attractions, world.get_history(), 4, type=Type.GREEDY))

    world.fill_world(agents, attractions)
    t = 1
    world.draw(t)
    world.clear_exports()
    while not world.park_empty():
        for attraction in attractions:
            attraction.advance_queue(t)
            attraction.calc_queue_time(t)
        for agent in agents:
            agent.update()
        if t % 10 == 0:
            print(t)
            world.draw(t)
            world.save(t, True)
        t += 1

    world.draw(t)
    world.save(t)
    world.build_gif()
    print(t)
    print(N)

    avg_queue_time = 0
    for attraction in attractions:
        avg_queue_time += attraction.get_avg_queue_time()
        #print(f'{attraction.__name} : {attraction.get_avg_queue_time()} ')

    print(f'Average queue time over all attractions: {avg_queue_time/len(attractions)}')


if __name__ == '__main__':
    do_profiling = True
    if do_profiling:
        with cProfile.Profile() as pr:
            run_model()

        with open('profiling_stats.txt', 'w') as stream:
            stats = Stats(pr, stream=stream)
            stats.strip_dirs()
            stats.sort_stats('time')
            stats.dump_stats('square.prof')
            stats.print_stats()
    else:
        run_model()