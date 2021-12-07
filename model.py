
from agent import Type
from world import World


class Model:
    def __init__(self, commit_prob=0.005) -> None:
        self.world = World()
        self.commit_prob = commit_prob
        pass

    def run_model(self):
        self.world.load_park("park_data.csv")

        self.world.populate(10, Type.NAIVE, self.commit_prob)
        t = 1
        self.world.draw(t)
        self.world.clear_exports()
        while not self.world.park_empty():
            for attraction in self.world.attractions:
                attraction.advance_queue(t)
                attraction.calc_queue_time(t)
            for agent in self.world.agents:
                agent.update()
            if t % 10 == 0:
                print(t)
                self.world.draw(t)
                self.world.save(t, True)
            t += 1

        self.world.draw(t)
        self.world.save(t)
        self.world.build_gif()
        print(t)
        print(self.world.n_agents)

        avg_queue_time = 0
        for attraction in self.world.attractions:
            avg_queue_time += attraction.get_avg_queue_time()
            #print(f'{attraction.__name} : {attraction.get_avg_queue_time()} ')

        print(f'Average queue time over all attractions: {avg_queue_time/len(self.world.attractions)}')

