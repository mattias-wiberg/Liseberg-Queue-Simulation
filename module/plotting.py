import pickle
from statistics import Statistics
import os
import sys
from agent import Type


delay = int(sys.argv[1])
mix_arg = sys.argv[2:]
mix = []
for i in range(0, len(mix_arg), 2):
    mix.append((Type.__getitem__(mix_arg[i]
                                 ), float(mix_arg[i+1])))
# Make logs folder
types, probs = list(zip(*mix))
folder_name = ""
for i in range(len(types)):
    folder_name += types[i].name + "_" + str(probs[i])
    if i != len(types)-1:
        folder_name += "-"
log_directory = "D://OneDrive - Chalmers tekniska hogskola"
log_directory += "/logs/"+folder_name+"/"+str(delay)+"/"

files = os.listdir(log_directory)
stats_filename = "statistics.p"
if stats_filename not in files:
    stats = Statistics(directory=log_directory)
else:
    with open(log_directory+stats_filename, "rb") as f:
        stats = pickle.load(f)

stats.display_stats()
# stats.plot_avg_queue_time()
# stats.plot_avg_std_queue_time()
# stats.plot_cum_queue_time_per_attraction()
# stats.plot_avg_num_agents_per_attraction()
# stats.plot_agent_cum()
# stats.plot_total_number_of_rides()
# stats.plot_n_rides_div_q_time()
# stats.plot_agent_fitness_by_type()

# stats.plot_num_agents_per_attraction()
# stats.plot_queue_time_per_attraction()

# stats.animate()
