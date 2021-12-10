import pickle
import random
from agent import State, Type
from world import World


class Model:
    # spawn_rules [(spawn_rate, start_time), (leave_rate, start_time)]
    extrapolate_pts = {0: 30, 30: 60, 60: 5*60, 5*60: 10*60,
                       10*60: 20*60, 20*60: 30*60, 30*60: 60*60, 60*60: 90*60}

    def __init__(self, mix, delay, commit_prob=0.005, spawn_rules=[(2.0834, 0), (4.1667, 39600)],
                 target_n_agents=15000, queue_prob=0.5, view_range=15, visit_window=3) -> None:
        self.mix = mix
        self.spawn_rule = spawn_rules[0]
        self.leave_rule = spawn_rules[1]

        types, probs = list(zip(*mix))
        if sum(probs) != 1:
            print("Error: Incorrect list of probabilities")

        world = World()
        world.load_park("../data/park_data.csv", delay,
                        Model.extrapolate_pts[delay])
        while world.n_agents < target_n_agents:
            choice = random.random()
            cum_prob = 0
            for i in range(len(probs)):
                cum_prob += probs[i]
                if cum_prob > choice:
                    type = types[i]
                    break
            world.spawn_agent(type, commit_prob, queue_prob,
                              view_range, visit_window)

        self.fractions = {}
        for type in types:
            self.fractions[type] = 0
        for agent in world.agents:
            self.fractions[agent.type] += agent.get_group_size()/world.n_agents

        print("Population Fractions:")
        for type in types:
            print(type.name, ":", round(self.fractions[type]*100, 4), "%")
        print("Using " + str(delay) + " seconds delay")
        self.spawn_list = world.agents
        self.n_agents = world.n_agents
        # Add first agent to start dynamics
        world.agents = [self.spawn_list.pop()]
        self.world = world

    # Print iterations progress
    def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                         (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()

    def run(self, time_steps, logs_path, save=True, draw=False, interactive=False, draw_export=False, draw_interval=5, save_interval=4, save_interval_max=1000):
        # Initial call to print 0% progress
        self.printProgressBar(
            0, time_steps, prefix='Progress:', suffix='Complete', length=50)
        t = 1
        cum_spawn = 0
        cum_leave = 0
        if draw:
            self.world.draw(t, interactive)
            if draw_export:
                self.world.save_png(t)
        agent_to_spawn = self.spawn_list.pop()
        for _ in range(time_steps):
            # Spawning
            if not len(self.spawn_list) == 0 and t > self.spawn_rule[1]:
                if cum_spawn >= agent_to_spawn.get_group_size():
                    cum_spawn -= agent_to_spawn.get_group_size()
                    self.world.agents.append(agent_to_spawn)
                    agent_to_spawn = self.spawn_list.pop()
                cum_spawn += self.spawn_rule[0]  # Add spawn rate to sum

            # Leaving prio FIFO of in park.
            if t > self.leave_rule[1]:
                if cum_leave >= 1:
                    for agent in self.world.agents:
                        if agent.state == State.IN_PARK:
                            if cum_leave >= agent.get_group_size():
                                agent.set_state(State.OUT_OF_PARK)
                                # self.world.agents.remove(agent)
                                cum_leave -= agent.get_group_size()
                            else:
                                break
                cum_leave += self.leave_rule[0]  # Add spawn rate to sum

            # Dynamics
            for attraction in self.world.attractions:
                attraction.advance_queue(t)
                attraction.calc_queue_time(t)

            for agent in self.world.agents:
                agent.update()

            if draw:
                if t % draw_interval == 0:
                    self.world.draw(t, interactive)
                    if draw_export:
                        self.world.save_png(t)

            if save:
                if t % save_interval == 0:
                    self.world.add_to_history()
                    if t % save_interval_max == 0:
                        self.world.dump(logs_path,
                                        "world"+format(int(t), "020b"))
                        self.world.history = []
            if t % 100:
                self.printProgressBar(
                    t + 1, time_steps, prefix='Progress:', suffix='Complete', length=50)
            t += 1

        if draw:
            self.world.draw(t, interactive)
            if draw_export:
                self.world.save_png(t)
        if save:
            self.world.dump(logs_path,
                            "world"+format(int(t), "020b"))
            with open(logs_path+"/model.p", "wb") as f:
                pickle.dump(self, f)
            self.world.history = []
        if draw_export:
            self.world.build_gif()
        # print(t)
        # print(self.world.n_agents)

        avg_queue_time = 0
        for attraction in self.world.attractions:
            avg_queue_time += attraction.get_avg_queue_time()
            #print(f'{attraction.name} : {attraction.get_avg_queue_time()} ')

        #print(f'Average queue time over all attractions: {avg_queue_time/len(self.world.attractions)}')
