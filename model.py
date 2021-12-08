from matplotlib.pyplot import angle_spectrum
from agent import Type
from world import World


class Model:
    def __init__(self, commit_prob=0.005, mix = [], n_agents=1000, draw = False, draw_interval=5) -> None:
        # TODO: Structure for type mix % of spawn prob
        self.world = World()
        self.n_agents = n_agents
        self.draw = draw
        self.draw_interval = draw_interval
        self.commit_prob = commit_prob

    def run(self):
        self.world.load_park("park_data.csv")

        self.world.populate(self.n_agents, Type.RANDOM, self.commit_prob)
        t = 1
        #self.world.clear_pngs()
        if self.draw: self.world.draw(t)
        #self.world.save_png(t)
        while not self.world.park_empty():
            for attraction in self.world.attractions:
                attraction.advance_queue(t)
                attraction.calc_queue_time(t)
            for agent in self.world.agents:
                agent.update()
            if t % self.draw_interval == 0:
                print(t)
                if self.draw: self.world.draw(t)
                #self.world.save_png(t)
                self.world.add_to_history()
            t += 1

        if self.draw: self.world.draw(t)
        self.world.add_to_history()
        #self.world.build_gif()
        self.world.dump("world")
        print(t)
        print(self.world.n_agents)

        avg_queue_time = 0
        for attraction in self.world.attractions:
            avg_queue_time += attraction.get_avg_queue_time()
            #print(f'{attraction.__name} : {attraction.get_avg_queue_time()} ')

        print(f'Average queue time over all attractions: {avg_queue_time/len(self.world.attractions)}')

