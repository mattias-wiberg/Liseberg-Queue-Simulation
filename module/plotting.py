import pickle
from statistics import Statistics
import os


log_directory = "../logs/0/0/"
files = os.listdir(log_directory)
stats_filename = "statistics.p"
if stats_filename not in files:
    stats = Statistics(directory=log_directory)
else:
    with open(log_directory+stats_filename, "rb") as f:
        stats = pickle.load(f)

stats.display_stats()
#stats.plot_avg_queue_time()
#stats.plot_avg_std_queue_time()
#stats.plot_cum_queue_time_per_attraction()
#stats.plot_avg_num_agents_per_attraction()
#stats.plot_agent_cum()
#stats.plot_total_number_of_rides()
#stats.plot_n_rides_div_q_time()
#stats.plot_agent_fitness_by_type()

#stats.plot_num_agents_per_attraction()
#stats.plot_queue_time_per_attraction()

#stats.animate()

