from agent import Agent
from attraction import Attraction
from behaviour import Type

agent1 = Agent((1,1), Type.NAIVE, 2)
agent2 = Agent((1,1), Type.NAIVE, 4)
agent3 = Agent((1,1), Type.NAIVE, 1)
agent4 = Agent((1,1), Type.NAIVE, 2)
agent5 = Agent((1,1), Type.NAIVE, 4)
agent6 = Agent((1,1), Type.NAIVE, 2)

attraction1 = Attraction(name="flumeride", attraction_coeff=1.0, wagon_size=4, wagon_ride_time=210, n_wagons=28, position=(1,1))

attraction1.add_to_queue(agent1)
attraction1.add_to_queue(agent2)
attraction1.add_to_queue(agent3)
attraction1.add_to_queue(agent4)
attraction1.add_to_queue(agent5)
attraction1.add_to_queue(agent6)

global_time = 1
queue_size = attraction1.get_queue_size()
while queue_size > 0:
    attraction1.advance_queue(global_time)
    print(f'Expected queue empty time: {attraction1.calc_queue_time(global_time)}')
    global_time += 1
    queue_size = attraction1.get_queue_size()

print(f"Queue empty at {global_time}")

