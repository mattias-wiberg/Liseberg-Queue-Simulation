import pickle
from statistics import Statistics

# average cum time in queue at every time step,
# histogram: changing with time for queue at every time period
# agents sorted by queue time and plotted as a distribution?

world = pickle.load(open("pickles/world.p", "rb"))
stats = Statistics(world)
#stats.plot_num_agents_per_attraction()
#stats.plot_queue_time_per_attraction()
#stats.plot_agent_cum()
stats.plot_cum_queue_time_per_attraction()

