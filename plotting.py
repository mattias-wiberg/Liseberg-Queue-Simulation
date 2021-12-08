import pickle
from statistics import Statistics

#cumulative number of agents at every attraction at every time step and also the number of agents not any attraction,
#average cum time in queue at every time step,

# histogram: changing with time for queue at every time period

world = pickle.load(open("pickles/world.p", "rb"))
stats = Statistics(world)
#stats.plot_num_agents_per_attraction()
#stats.plot_queue_time_per_attraction()
stats.plot_agent_cum()

"""
queue_time_histories = list(map(lambda attraction : attraction.get_queue_time_history(), attractions))
for t, world_at_t in enumerate(world.get_history()):
    agents = world_at_t[0]
    attractions = world_at_t[1]

    x = 5
"""
