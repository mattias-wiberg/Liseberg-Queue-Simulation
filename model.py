
from matplotlib.pyplot import angle_spectrum
from agent import Type
from world import World
import multiprocessing as mp

class Model:
    def __init__(self, commit_prob=0.005, mix = []) -> None:
        # TODO: Structure for type mix % of spawn prob
        self.world = World()
        self.commit_prob = commit_prob
        pass

    def run_model(self):
        self.world.load_park("park_data.csv")

        self.world.populate(1000, Type.NAIVE, self.commit_prob)
        t = 1
        #self.world.clear_pngs()
        #self.world.draw(t)
        #self.world.save_png(t)
        while not self.world.park_empty():
            for attraction in self.world.attractions:
                attraction.advance_queue(t)
                attraction.calc_queue_time(t)
            #for agent in self.world.agents:
            #    agent.update()
            with mp.Pool(mp.cpu_count()) as pool:
                pool.map(lambda x:x.update(), self.world.agents)
            if t % 10 == 0:
                print(t)
                #self.world.draw(t, False)
                #self.world.save_png(t)
                self.world.add_to_history()
            t += 1

        #self.world.draw(t)
        self.world.add_to_history()
        #self.world.build_gif()
        print(t)
        print(self.world.n_agents)

        avg_queue_time = 0
        for attraction in self.world.attractions:
            avg_queue_time += attraction.get_avg_queue_time()
            #print(f'{attraction.__name} : {attraction.get_avg_queue_time()} ')

        print(f'Average queue time over all attractions: {avg_queue_time/len(self.world.attractions)}')

