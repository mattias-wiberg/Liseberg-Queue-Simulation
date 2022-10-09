# Liseberg Queue Simulation
 Simulation of liseberg queue simulation of the delayed info about queue times 
![Simulaton](https://github.com/mattias-wiberg/Liseberg-Queue-Simulation/blob/main/Types/NAIVE/naive0.gif?raw=true)
# Run
plotting/animation:
    avg total queue time
    avg queue time by agent type
    avg queue time per attraction

## Simulation
time_step = int
world_history = list(World)

### World
agents = list(Agent)
attractions = list(Attraction)

#### Agent
id = int
position = x,y
type = Type
target = Attraction # Attraction
visited_attractions = dict(str:list(float)) # attraction strs

visibility = float # Cone?
congestion_radius = float # Cone? maybe only in front
velocity = float   # dependent och congestion
direction = float

state = {}

##### Type
# eg. Flume ride bois, extrapolating, visited everything, when they leave
id = int (Different logic)
group = Group # the group it is part of
time_until_toilet = int
time_until_food = int
leaving_condition
commit_prob = float

#### Attraction
attraction_coeff = float
ride_size = int
ride_time = int
position = x, y
queue = queue(Agents)
queue_history = list(int)  # length delay, time history calculate w.r.t. ride time and size
name = str

# Execution sequence
- Agents close enough to enter queue
- Advance queue: Attraction.advance_queue(global_time)
- Calculate queue time: Attraction.calc_queue_time(global_time)
(NOTE: very important for this to be called after advance queue due to th ecalculate nearest modulo time implementation in calc_queue_time)
- Move agents

