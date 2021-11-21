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
        self.__name = name
        self.__attraction_coeff = attraction_coeff
        self.__ride_size = ride_size
        self.__ride_time = ride_time
        self.__position = position
        self.__queue = []
        self.__queue_time = 0

    def add_to_queue(self, agent):
        self.__queue.append(agent)
        self.__queue_time += (agent.get_group_size()*self.__ride_time)

    def advance_queue(self):
        places_left = self.__ride_size

        while places_left > 0:
            next_in_line = self.__queue[0].get_group_size()


    def remove_from_queue(self, idx=0):
        return self.__queue.pop(idx)

    

        


