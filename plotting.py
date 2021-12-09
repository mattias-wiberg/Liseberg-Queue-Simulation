import pickle
from statistics import Statistics

# average cum time in queue at every time step,
# histogram: changing with time for queue at every time period
# agents sorted by queue time and plotted as a distribution?

world = pickle.load(open("pickles/world00001.p", "rb"))
stats = Statistics(world)
#stats.plot_num_agents_per_attraction()
#stats.plot_queue_time_per_attraction()
#stats.plot_agent_cum()
#stats.plot_cum_queue_time_per_attraction()
#stats.plot_avg_queue_time()
#stats.plot_agent_fitness_by_type()
#stats.plot_total_number_of_rides()
stats.plot_n_rides_div_q_time()

