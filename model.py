import random
from agent import State, Type
from world import World


class Model:
    # spawn_rules [(spawn_rate, start_time), (leave_rate, start_time)]
    def __init__(self, commit_prob=0.005, spawn_rules=[(1,0), (1, 10000)], mix = [(Type.NAIVE, 1)],
    target_n_agents=1000, queue_prob = 0.5, view_range=15, visit_window=3, delay=0, extrapolate_pts=60) -> None:
        self.mix = mix
        self.spawn_rule = spawn_rules[0]
        self.leave_rule = spawn_rules[1]

        types, probs = list(zip(*mix))
        if sum(probs) != 1:
            print("Error: Incorrect list of probabilities")
        
        world = World()
        world.load_park("park_data.csv", delay, extrapolate_pts)
        while world.n_agents < target_n_agents:
            choice = random.random()
            cum_prob = 0
            for i in range(len(probs)):
                cum_prob += probs[i]
                if cum_prob > choice:
                    type = types[i]
                    break
            world.spawn_agent(type, commit_prob, queue_prob, view_range, visit_window)

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

    def run(self, time_steps, save=True, draw=False, interactive=False, draw_export=False, draw_interval=5, save_interval=1, save_interval_max=1000):
        t = 1
        cum_spawn = 0
        cum_leave = 0
        if draw: 
            self.world.draw(t, interactive)
            if draw_export: self.world.save_png(t)
        agent_to_spawn = self.spawn_list.pop()
        for _ in range(time_steps):
            # Spawning
            if not len(self.spawn_list)==0 and t > self.spawn_rule[1]:
                if cum_spawn >= agent_to_spawn.get_group_size():
                    cum_spawn -= agent_to_spawn.get_group_size()
                    self.world.agents.append(agent_to_spawn)
                    agent_to_spawn = self.spawn_list.pop()
                cum_spawn += self.spawn_rule[0] # Add spawn rate to sum

            # Leaving prio FIFO of in park.
            if t > self.leave_rule[1]:
                if cum_leave >= 1:
                    for agent in self.world.agents:
                        if agent.state == State.IN_PARK:
                            if cum_leave >= agent.get_group_size():
                                agent.set_state(State.OUT_OF_PARK)
                                #self.world.agents.remove(agent)
                                cum_leave -= agent.get_group_size()
                            else:
                                break
                cum_leave += self.leave_rule[0] # Add spawn rate to sum

            # Dynamics
            for attraction in self.world.attractions:
                attraction.advance_queue(t)
                attraction.calc_queue_time(t)

            for agent in self.world.agents:
                agent.update()

            if draw: 
                if t % draw_interval == 0:
                    self.world.draw(t, interactive)
                    if draw_export: self.world.save_png(t)
                    
            if save:
                if t % save_interval == 0:
                    self.world.add_to_history()
                    if t % save_interval_max == 0:
                        self.world.dump("world"+format(int(t/save_interval_max), "05b"))
                        self.world.history = []
                    
            print(t)
            t += 1

        if draw:
            self.world.draw(t, interactive)
            if draw_export: self.world.save_png(t)
            

        if draw_export: self.world.build_gif()
        print(t)
        print(self.world.n_agents)

        avg_queue_time = 0
        for attraction in self.world.attractions:
            avg_queue_time += attraction.get_avg_queue_time()
            #print(f'{attraction.name} : {attraction.get_avg_queue_time()} ')

        print(f'Average queue time over all attractions: {avg_queue_time/len(self.world.attractions)}')

