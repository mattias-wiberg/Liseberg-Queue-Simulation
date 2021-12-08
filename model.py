import random
from matplotlib.pyplot import angle_spectrum, gray
from agent import Agent, Type
from world import World


class Model:
    def __init__(self, commit_prob=0.005, mix = [(Type.NAIVE, 1)], target_n_agents=1000, draw = False, draw_interval=5, queue_prob = 0.5, view_range=15) -> None:
        self.draw = draw
        self.draw_interval = draw_interval
        self.mix = mix

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
        self.world = world
        self.n_agents = world.n_agents

    def run(self):
        t = 1
        if self.draw: self.world.draw(t)
        while not self.world.park_empty():
            for attraction in self.world.attractions:
                attraction.advance_queue(t)
                attraction.calc_queue_time(t)
            for agent in self.world.agents:
                agent.update()
            if t % self.draw_interval == 0:
                print(t)
                if self.draw: self.world.draw(t)
                self.world.add_to_history()
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

