from agent import Agent
from attraction import Attraction
from behaviour import Type
from world import World

x = 5

print("Hello world")
agent1 = Agent((1.2,1), Type.NAIVE, 2)
agent2 = Agent((1,1.2), Type.NAIVE, 2)
agent3 = Agent((1.5,1.5), Type.NAIVE, 2)

attraction1 = Attraction(name="flumeride", attraction_coeff=1.0, wagon_size=4, wagon_ride_time=180, n_wagons=10, position=(1,1))
attraction2 = Attraction(name="flumeride", attraction_coeff=1.0, wagon_size=4, wagon_ride_time=180, n_wagons=10, position=(2,1))
attraction3 = Attraction(name="flumeride", attraction_coeff=1.0, wagon_size=4, wagon_ride_time=180, n_wagons=10, position=(2,2))
world = World([agent1, agent2, agent3], [attraction1, attraction2, attraction3])
world.draw()

