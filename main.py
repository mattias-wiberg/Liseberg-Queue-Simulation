from agent import Agent
from attraction import Attraction
from agentType import Type

x = 5

print("Hello world")
aT1 = Type(0.8)
agent1 = Agent((1,1), aT1)
#agent2 = Agent()
#agent3 = Agent()

attraction1 = Attraction(name="flumeride", attraction_coeff=1.0, ride_size=4, ride_time=180, position=(1,1))

attraction1.add_to_queue(1)
attraction1.add_to_queue(3)
attraction1.add_to_queue(9)

a = attraction1.remove_from_queue()
a = attraction1.remove_from_queue()
a = attraction1.remove_from_queue()

