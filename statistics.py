import matplotlib.pyplot as plt
import numpy as np

class Statistics():
    def __init__(self, world):
        self.world = world
        self.attraction_names = ["Helix", "AtmosFear", "Lisebergsbanan", "Loke", "Balder", 
        "Valkyria", "Mechanica", "FlumeRide", "Hanghai", "Aerospin", "Slänggungan"] 
        # pickle has trouble with non-ASCII characters, so that is why the names are here
        self.time_values = list(range(len(self.world.get_history())))
        self.history = self.world.get_history()
        self.fig, self.ax = plt.subplots()
        plt.draw()

    def plot_queue_time_per_attraction(self):
        queue_time_history = []
        for time_step in range(len(self.time_values)):
            attractions = self.history[time_step][1]
            queue_time_history.append(list(map(lambda attraction:attraction.get_queue_time_history()[-1], attractions)))
        queue_time_history = np.array(queue_time_history)

        plt.clf()
        for i, attraction_name in enumerate(self.attraction_names):
            plt.plot(self.time_values, queue_time_history[:,i], label = attraction_name)

        plt.xlabel('Time Step [s]')
        plt.ylabel('Queue Time [s]')
        plt.title('Queue Time Per Attraction')
        plt.legend()
        plt.show()
    
    def plot_num_agents_per_attraction(self):
        
        num_agents_history = []
        for time_step in range(len(self.time_values)):
            attractions = self.history[time_step][1]
            num_agents = list(map(lambda attraction:attraction.get_num_agents(), attractions))
            num_agents_history.append(num_agents)
        num_agents_history = np.array(num_agents_history)

        plt.clf()
        for i, attraction_name in enumerate(self.attraction_names):
            plt.plot(self.time_values, num_agents_history[:,i], label = attraction_name)

        plt.xlabel('Time Step [s]')
        plt.ylabel('Number of Agents')
        plt.title('Number of Agents Per Attraction')
        plt.legend()
        plt.show()



