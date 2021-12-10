import pickle
from statistics import Statistics
import os

log_directory = "logs/"
files = os.listdir(log_directory)
stats_filename = "statistics.p" 
if stats_filename not in files:
    stats = Statistics()
else:
    with open(log_directory+stats_filename, "rb") as f:
        stats = pickle.load(f)

#stats.plot_num_agents_per_attraction()
#stats.plot_queue_time_per_attraction()
#stats.plot_agent_cum()
#stats.plot_cum_queue_time_per_attraction()
#stats.plot_avg_queue_time()
#stats.plot_agent_fitness_by_type()
#stats.plot_total_number_of_rides()
#stats.plot_n_rides_div_q_time()
#stats.plot_avg_std_queue_time()
