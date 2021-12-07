
from agent import Type
from world import World


class Model:
    def __init__(self) -> None:
        pass

    def run_model(self):
        agents = []
        world = World()
        world.load_park("park-data.csv")

        world.populate(10,Type.)
        t = 1
        world.draw(t)
        world.clear_exports()
        while not world.park_empty():
            for attraction in attractions:
                attraction.advance_queue(t)
                attraction.calc_queue_time(t)
            for agent in agents:
                agent.update()
            if t % 10 == 0:
                print(t)
                world.draw(t)
                world.save(t, True)
            t += 1

        world.draw(t)
        world.save(t)
        world.build_gif()
        print(t)
        print(world.n_agents)

        avg_queue_time = 0
        for attraction in attractions:
            avg_queue_time += attraction.get_avg_queue_time()
            #print(f'{attraction.__name} : {attraction.get_avg_queue_time()} ')

        print(f'Average queue time over all attractions: {avg_queue_time/len(attractions)}')

