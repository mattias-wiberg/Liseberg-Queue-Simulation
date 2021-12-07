import matplotlib.pyplot as plt

class Statistics():
    def __init__(self, world):
        self.world = world
        self.attraction_names = ["Helix", "AtmosFear", "Lisebergsbanan", "Loke", "Balder", 
        "Valkyria", "Mechanica", "FlumeRide", "Hanghai", "Aerospin", "Slänggungan"] 
        # pickle has trouble with non-ASCII characters, so that is why the names are here

    def plot_queue_time_per_attraction(self):
        attractions = self.world.get_history()[-1][1]
        time_values = list(range(len(attractions[0].get_queue_time_history())))

        plt.clf()
        for i, attraction in enumerate(attractions):
            plt.plot(time_values, attraction.get_queue_time_history(), label = self.attraction_names[i])

        plt.xlabel('Time Step [s]')
        plt.ylabel('Queue Time [s]')
        plt.title('Queue Time Per Attraction')
        plt.legend()
        plt.show()
    
    def plot_num_agents_per_attraction(self):
        
        num_agents_history = []
        for time_step in self.world.get_history():
            attractions = time_step[1]
            num_agents = []
            for attraction in attractions:
                num_agents.append(attraction.get_num_agents())
            num_agents_history.append(num_agents)
            
            #num_agents.append(list(map(lambda attraction : attraction.get_num_agents(), attractions)))
        

        #num_agents = list(map(lambda time_step : list(map(lambda attraction : attraction.get_num_agents(), time_step[1])), self.world.get_history()))
        #num_agents = list(map(lambda time_step : time_step[1].get_num_agents(), self.world.get_history()))

        x = 5


