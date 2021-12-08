import random
from matplotlib.pyplot import angle_spectrum, gray
from numpy import empty
from agent import Agent, State, Type
from world import World


class Model:
    # spawn_rules [(spawn_rate, start_time), (leave_rate, start_time)]
    def __init__(self, commit_prob=0.005, spawn_rules=[(0.1,0), (0.1,1000)], mix = [(Type.NAIVE, 1)], target_n_agents=1000, draw = False, draw_interval=5, queue_prob = 0.5, view_range=15) -> None:
        self.draw = draw
        self.draw_interval = draw_interval
        self.mix = mix
        self.spawn_rule = spawn_rules[0]
        self.leave_rule = spawn_rules[1]

        types, probs = list(zip(*mix))
        if sum(probs) != 1:
            print("Error: Incorrect list of probabilities")
        
        world = World()
        world.load_park("park_data.csv")
        while world.n_agents < target_n_agents:
            choice = random.random()
            cum_prob = 0
            for i in range(len(probs)):
                cum_prob += probs[i]
                if cum_prob > choice:
                    type = types[i]
                    break
            world.spawn_agent(type, commit_prob, queue_prob, view_range)

        fractions = {}
        for type in types:
            fractions[type] = 0
        for agent in world.agents:
            fractions[agent.type] += agent.get_group_size()/world.n_agents
        
        print("Population Fractions:")
        for type in types:
            print(type.name,":",round(fractions[type]*100,4),"%")
        
        self.spawn_list = world.agents
        self.n_agents = world.n_agents
        world.agents = [self.spawn_list.pop()] # Add first agent to start dynamics
        self.world = world

    def run(self):
        t = 1
        cum_spawn = 0
        cum_leave = 0
        if self.draw: self.world.draw(t)
        agent_to_spawn = self.spawn_list.pop()
        while True:
            # Spawning
            if not len(self.spawn_list)==0 and t > self.spawn_rule[1]:
                if cum_spawn >= agent_to_spawn.get_group_size():
                    cum_spawn -= agent_to_spawn.get_group_size()
                    self.world.agents.append(agent_to_spawn)
                    agent_to_spawn = self.spawn_list.pop()
                cum_spawn += self.spawn_rule[0] # Add spawn rate to sum

            # Leaving
            if t > self.leave_rule[1]:
                if cum_leave >= 1:
                    for agent in self.world.agents:
                        if agent.state == State.IN_PARK and cum_leave >= agent.get_group_size():
                            self.world.agents.remove(agent)
                            cum_leave -= agent.get_group_size()
                            if cum_leave < 1:
                                break
                cum_leave += self.leave_rule[0] # Add spawn rate to sum

            # Dynamics
            for attraction in self.world.attractions:
                attraction.advance_queue(t)
                attraction.calc_queue_time(t)

            for agent in self.world.agents:
                agent.update()

            if t % self.draw_interval == 0:
                print(t)
                if self.draw: self.world.draw(t)
                self.world.add_to_history()

            if self.world.park_empty():
                break
            t += 1

        if self.draw: self.world.draw(t)
        self.world.add_to_history()
        self.world.dump("world")
        print(t)
        print(self.world.n_agents)

        avg_queue_time = 0
        for attraction in self.world.attractions:
            avg_queue_time += attraction.get_avg_queue_time()
            #print(f'{attraction.__name} : {attraction.get_avg_queue_time()} ')

        print(f'Average queue time over all attractions: {avg_queue_time/len(self.world.attractions)}')

