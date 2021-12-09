import matplotlib.pyplot as plt
import numpy as np

class Statistics():
    def __calc_queue_time_per_attraction(self):
        queue_time_history = []
        for time_step in range(len(self.time_values)):
            attractions = self.history[time_step][1]
            queue_time_history.append(list(map(lambda attraction:attraction.get_queue_time_history()[-1], attractions)))
        return np.array(queue_time_history)

    def __calc_num_agents_per_attraction(self):
        num_agents_history = []
        for time_step in range(len(self.time_values)):
            attractions = self.history[time_step][1]
            num_agents = list(map(lambda attraction:attraction.get_num_agents(), attractions))
            num_agents_history.append(num_agents)
        return np.array(num_agents_history)
    
    def __init__(self, world):
        self.world = world
        self.attraction_names = ["Helix", "AtmosFear", "Lisebergsbanan", "Loke", "Balder", 
        "Valkyria", "Mechanica", "FlumeRide", "Hanghai", "Aerospin", "Slänggungan"] 
        # pickle has trouble with non-ASCII characters, so that is why the names are here
        self.time_values = list(range(len(self.world.get_history())))
        self.history = self.world.get_history()
        self.total_num_people = sum(list(map(lambda agent:agent.get_group_size(), self.history[0][0])))

        self.queue_time_history = self.__calc_queue_time_per_attraction()
        self.num_agents_history = self.__calc_num_agents_per_attraction()

    def plot_cum_queue_time_per_attraction(self):
        # to get the real cumulative queue time, multiply the cum_queue_time array with the time_step size
        # right now the unit is number of time steps waited in queue
        cum_queue_time = np.zeros( (len(self.time_values), len(self.attraction_names)) )
        cum_queue_time[0,:] = self.num_agents_history[0,:]
        for time_step in range(1, len(self.time_values)):
            cum_queue_time[time_step,:] = self.num_agents_history[time_step,:] + cum_queue_time[time_step-1,:]
        cum_queue_time = np.array(cum_queue_time)

        plt.clf()
        for i, attraction_name in enumerate(self.attraction_names):
            plt.plot(self.time_values, cum_queue_time[:,i], label = attraction_name)

        plt.xlabel('Time Step')
        plt.ylabel('Cumulative Queue Time [number of timesteps]')
        plt.title('Cumulative Queue Time Per Attraction')
        plt.legend()
        plt.show()


    def plot_queue_time_per_attraction(self):
        # TODO: animated histo plot instead
        plt.clf()
        for i, attraction_name in enumerate(self.attraction_names):
            plt.plot(self.time_values, self.queue_time_history[:,i], label = attraction_name)

        plt.xlabel('Time Step')
        plt.ylabel('Queue Time [number of timesteps]')
        plt.title('Queue Time Per Attraction')
        plt.legend()
        plt.show()
    
    def plot_num_agents_per_attraction(self):
        # TODO: animated histo plot instead
        num_agents_in_attractions = np.sum(self.num_agents_history, axis=1)
        num_agents_in_park = np.array(self.total_num_people) - num_agents_in_attractions

        plt.clf()
        for i, attraction_name in enumerate(self.attraction_names):
            plt.plot(self.time_values, self.num_agents_history[:,i], label = attraction_name)
        
        plt.plot(self.time_values, num_agents_in_park, label = "Not In Attraction")

        plt.xlabel('Time Step')
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

        plt.xlabel('Time Step')
        plt.ylabel('Cumulative Number of Agents')
        plt.title('Cumulative Number of Agents Per Attraction')
        plt.legend()
        plt.show()

    def plot_avg_queue_time(self):
        avg_queue_times = np.zeros( (len(self.time_values), len(self.attraction_names)) )
        avg_queue_times[0,:] = self.queue_time_history[0,:]
        for time_step in range(1, len(self.time_values)):
            avg_queue_times[time_step,:] = np.average(self.queue_time_history[:time_step+1,:], axis=0)
        avg_queue_times = np.array(avg_queue_times)
        
        plt.clf()
        for i, attraction_name in enumerate(self.attraction_names):
            plt.plot(self.time_values, avg_queue_times[:,i], label = attraction_name)

        plt.xlabel('Time Step')
        plt.ylabel('Average Queue Time [number of timesteps]')
        plt.title('Avergae Queue Time Per Attraction')
        plt.legend()
        plt.show()        

