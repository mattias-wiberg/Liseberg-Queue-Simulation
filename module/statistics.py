import matplotlib.pyplot as plt
import numpy as np
from agent import Type, State
import pickle
import os


class Statistics():
    def __calc_queue_time_per_attraction(self):
        queue_time_history = []
        for time_step in range(len(self.time_values)):
            attractions = self.history[time_step][1]
            queue_time_history.append(list(
                map(lambda attraction: attraction.get_queue_time_history()[-1], attractions)))
        return np.array(queue_time_history)

    def __calc_num_agents_per_attraction(self):
        num_agents_history = []
        for time_step in range(len(self.time_values)):
            attractions = self.history[time_step][1]
            num_agents = list(
                map(lambda attraction: attraction.get_num_agents(), attractions))
            num_agents_history.append(num_agents)
        return np.array(num_agents_history)

    def __calc_cum_num_agents_per_attraction(self):
        attraction_pickled_names = list(
            map(lambda attraction: attraction.get_name(), self.history[0][1]))

        agent_cum = []
        for time_step in range(len(self.time_values)):

            agent_cum_at_t = {}
            for attraction_name in attraction_pickled_names:
                agent_cum_at_t[attraction_name] = 0

            agents = self.history[time_step][0]
            for agent in agents:
                for visited_attraction in agent.visited:
                    agent_cum_at_t[visited_attraction.get_name()
                                   ] += agent.get_group_size()

            agent_cum.append(list(agent_cum_at_t.values()))
        return np.array(agent_cum)

    def __calc_cum_queue_time_per_attraction(self):
        # DOES NOT INCLUDE PEOPLE IN WAGONS!
        cum_queue_time = np.zeros(
            (len(self.time_values), len(self.attraction_names)))
        attractions = self.history[0][1]
        cum_queue_time[0, :] = np.array(
            list(map(lambda attraction: attraction.queue_size, attractions)))

        for time_step in range(1, len(self.time_values)):
            attractions = self.history[time_step][1]
            cum_queue_time[time_step, :] = np.array(list(map(
                lambda attraction: attraction.queue_size, attractions))) + cum_queue_time[time_step-1, :]

        return cum_queue_time

    def __calc_avg_queue_times(self):
        avg_queue_times = np.zeros(
            (len(self.time_values), len(self.attraction_names)))
        avg_queue_times[0, :] = self.queue_time_history[0, :]
        for time_step in range(1, len(self.time_values)):
            avg_queue_times[time_step, :] = np.average(
                self.queue_time_history[:time_step+1, :], axis=0)

        return np.array(avg_queue_times)

    def __calc_std_avg_queue_times_all_attractions(self):
        std_queue_times = np.zeros((len(self.time_values), 1))
        std_queue_times[0, :] = self.avg_queue_times_all_attractions[0]
        for time_step in range(1, len(self.time_values)):
            std_queue_times[time_step] = np.std(
                self.avg_queue_times_all_attractions[:time_step+1], axis=0)
        std_queue_times = np.reshape(std_queue_times, newshape=(1000,))
        return std_queue_times

    def __calc_total_num_people_history(self):
        num_people_history = np.zeros((len(self.time_values), 1))
        for time_step in range(len(self.time_values)):
            num_people_history[time_step, :] = sum(
                list(map(lambda agent: agent.get_group_size(), self.history[time_step][0])))
        num_people_history = np.reshape(num_people_history, newshape=(1000,))
        return num_people_history

    def __calc_agent_fitness_by_type(self):
        # agent fitness defined as sum visited attractions/sum cumulative queue time
        # by type and by group size
        num_attractions_by_type = np.zeros(
            (4, len(Type)))   # Row: size, Col: Type
        cum_queue_time_by_type = np.zeros((4, len(Type)))

        agents = self.history[-1][0]
        for agent in agents:
            num_attractions_by_type[agent.get_group_size(
            )-1, agent.type.value-1] += len(agent.visited)

        for time_step in range(len(self.time_values)):
            agents = self.history[time_step][0]
            for agent in agents:
                if agent.state == State.IN_QUEUE:
                    # in number of timesteps, so add 1
                    cum_queue_time_by_type[agent.get_group_size(
                    )-1, agent.type.value-1] += 1

        fitness_score_by_size_by_type = np.zeros((4, len(Type)))
        for iSize in range(np.shape(fitness_score_by_size_by_type)[0]):
            for jType in range(np.shape(fitness_score_by_size_by_type)[1]):
                num_visited_attractions = num_attractions_by_type[iSize, jType]
                if num_visited_attractions != 0:
                    fitness_score_by_size_by_type[iSize, jType] = num_visited_attractions / \
                        cum_queue_time_by_type[iSize, jType]

        return fitness_score_by_size_by_type

    def __init__(self, directory="logs/"):
        self.pickle_files = os.listdir(directory)
        self.attraction_names = ["Helix", "AtmosFear", "Lisebergsbanan", "Loke", "Balder",
                                 "Valkyria", "Mechanica", "FlumeRide", "Hanghai", "Aerospin", "Slänggungan"]
        # pickle has trouble with non-ASCII characters, so that is why the names are here

        self.queue_time_history = []
        self.num_agents_history = []
        self.cum_num_agents_history = []
        self.cum_queue_time_per_attraction = []
        self.total_num_people_history = []
        self.fitness_score_by_size_by_type = []
        self.time_values_list = []

        i_max = len(self.pickle_files)
        for i,file in enumerate(self.pickle_files):
            self.history = pickle.load(open(directory+file, "rb"))
            self.time_values = list(range(len(self.history)))

            self.queue_time_history.append(self.__calc_queue_time_per_attraction())
            self.num_agents_history.append(self.__calc_num_agents_per_attraction())
            self.cum_num_agents_history.append(self.__calc_cum_num_agents_per_attraction())
            self.cum_queue_time_per_attraction.append(self.__calc_cum_queue_time_per_attraction())
            self.total_num_people_history.append(self.__calc_total_num_people_history())
            self.fitness_score_by_size_by_type.append(self.__calc_agent_fitness_by_type())
            self.time_values_list.append(self.time_values)
            print(f'{i}/{i_max}')

        self.time_values = list(range(len(self.time_values_list)))

        self.total_n_rides = np.sum(self.cum_num_agents_history, axis=1)
        self.total_queue_time = np.sum(self.cum_queue_time_per_attraction, axis=1)
        self.avg_queue_times = self.__calc_avg_queue_times()
        self.avg_queue_times_all_attractions = np.average(self.avg_queue_times, axis=1)
        self.std_avg_queue_times_all_attractions = self.__calc_std_avg_queue_times_all_attractions()


    def plot_cum_queue_time_per_attraction(self):
        # DOES NOT INCLUDE PEOPLE IN WAGONS!
        plt.clf()
        for i, attraction_name in enumerate(self.attraction_names):
            plt.plot(
                self.time_values, self.cum_queue_time_per_attraction[:, i], label=attraction_name)

        plt.xlabel('Time Step')
        plt.ylabel('Cumulative Queue Time [number of timesteps]')
        plt.title('Cumulative Queue Time Per Attraction')
        plt.legend()
        plt.show()

    def plot_queue_time_per_attraction(self):
        # TODO: animated histo plot instead
        plt.clf()
        for i, attraction_name in enumerate(self.attraction_names):
            plt.plot(self.time_values,
                     self.queue_time_history[:, i], label=attraction_name)

        plt.xlabel('Time Step')
        plt.ylabel('Queue Time [number of timesteps]')
        plt.title('Queue Time Per Attraction')
        plt.legend()
        plt.show()

    def plot_num_agents_per_attraction(self):
        # TODO: animated histo plot instead
        # TAKES GROUP SIZE INTO ACCOUNT AND BOTH THE AGENTS IN WAGONS AND QUEUE
        num_agents_in_attractions = np.sum(self.num_agents_history, axis=1)
        num_agents_in_park = self.total_num_people_history - num_agents_in_attractions

        plt.clf()
        for i, attraction_name in enumerate(self.attraction_names):
            plt.plot(self.time_values,
                     self.num_agents_history[:, i], label=attraction_name)

        plt.plot(self.time_values, num_agents_in_park,
                 label="Not In Attraction")

        plt.xlabel('Time Step')
        plt.ylabel('Number of Agents')
        plt.title('Number of Agents Per Attraction')
        plt.legend()
        plt.show()

    def plot_agent_cum(self):
        plt.clf()
        for i, attraction_name in enumerate(self.attraction_names):
            plt.plot(self.time_values,
                     self.cum_num_agents_history[:, i], label=attraction_name)

        plt.xlabel('Time Step')
        plt.ylabel('Cumulative Number of Agents')
        plt.title('Cumulative Number of Agents Per Attraction')
        plt.legend()
        plt.show()

    def plot_total_number_of_rides(self):
        plt.clf()
        plt.plot(self.time_values, self.total_n_rides)
        plt.xlabel('Time Step')
        plt.ylabel('Total Number of Rides')
        plt.title('Total Number of Rides Over All The Attractions')
        plt.show()

    def plot_avg_queue_time(self):
        plt.clf()
        for i, attraction_name in enumerate(self.attraction_names):
            plt.plot(self.time_values,
                     self.avg_queue_times[:, i], label=attraction_name)

        plt.xlabel('Time Step')
        plt.ylabel('Average Queue Time [number of timesteps]')
        plt.title('Average Queue Time Per Attraction')
        plt.legend()
        plt.show()

    def plot_agent_fitness_by_type(self):
        # agent fitness defined as sum visited attractions/sum cumulative queue time
        # by type and by group size
        plt.imshow(self.fitness_score_by_size_by_type,
                   cmap='binary', interpolation='nearest')
        plt.colorbar()
        plt.xlabel('Agent Type')
        plt.ylabel('Group Size')
        plt.title('Fitness Score Per Agent Type and Group Size')
        plt.show()

    def plot_n_rides_div_q_time(self):
        # sum all rides/sum cumulative queue time
        plt.clf()
        n_rides_div_q_time = self.total_n_rides/self.total_queue_time
        n_rides_div_q_time = np.nan_to_num(n_rides_div_q_time)
        plt.plot(self.time_values, n_rides_div_q_time)
        plt.xlabel('Time Step')
        plt.ylabel(
            'Total Number of All Rides / Cumulative Queue Over All Attractions')
        plt.title(
            'Total Number of All Rides / Cumulative Queue Over All Attractions')
        plt.show()

    def plot_avg_std_queue_time(self):
        plt.clf()
        plt.plot(self.time_values, self.avg_queue_times_all_attractions,
                 label="Average Queue Time")
        plt.plot(self.time_values, self.std_avg_queue_times_all_attractions,
                 label="Std of The Average Queue Time")
        plt.xlabel('Time Step')
        plt.ylabel('Value')
        plt.title(
            'Average Queue Time Over All Attractions and Standard Deviation of Said Average')
        plt.legend()
        plt.show()
