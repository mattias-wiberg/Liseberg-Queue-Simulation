class Attraction:
    """
    attraction_coeff = float
    ride_size = int
    ride_time = int
    position = x, y
    queue = queue(Agents)
    queue_history = list(int)  # length delay, time history calculate w.r.t. ride time and size
    name = str
    """

    def __init__(self, name:str, attraction_coeff:float, ride_size:int, ride_time:float, position:tuple):
        self.name = name
        self.attraction_coeff = attraction_coeff
        self.ride_size = ride_size
        self.ride_time = ride_time
        self.position = position
        self.queue = []
        

    def add_to_queue(self, agent):
        self.queue.append(agent)

    def remove_from_queue(self, idx=0):
        return self.queue.pop(idx)

    

        


