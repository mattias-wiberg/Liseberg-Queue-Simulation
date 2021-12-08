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

    def plot_queue_time_per_attraction(self):
        # TODO: animated histo plot instead
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
        # TODO: animated histo plot instead
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

    def plot_agent_cum(self):
        # TODO: animated histo plot instead
        attraction_pickled_names = list(map(lambda attraction:attraction.get_name(), self.history[0][1]))

        agent_cum = []
        for time_step in range(len(self.time_values)):
            
            agent_cum_at_t = {}
            for attraction_name in attraction_pickled_names:
                agent_cum_at_t[attraction_name] = 0

            agents = self.history[time_step][0]
            for agent in agents:
                for visited_attraction in agent.visited:
                    agent_cum_at_t[visited_attraction.get_name()] += agent.get_group_size()

            agent_cum.append(list(agent_cum_at_t.values()))
        agent_cum = np.array(agent_cum)
        
        plt.clf()
        for i, attraction_name in enumerate(self.attraction_names):
            plt.plot(self.time_values, agent_cum[:,i], label = attraction_name)

        plt.xlabel('Time Step [s]')
        plt.ylabel('Cumulative Number of Agents')
        plt.title('Cumulative Number of Agents Per Attraction')
        plt.legend()
        plt.show()


