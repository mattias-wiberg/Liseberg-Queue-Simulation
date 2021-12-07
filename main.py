import random
from typing import List
from agent import Agent, Type
from attraction import Attraction
from model import Model
from spawn import Spawn
from world import World
import numpy as np
from matplotlib import pyplot as plt
import cProfile
from pstats import Stats, SortKey
import pickle
np.random.seed(10)
random.seed(10)

if __name__ == '__main__':
    model = Model()

    do_profiling = False
    if do_profiling:
        with cProfile.Profile() as pr:
            model.run_model()

        with open('profiling_stats.txt', 'w') as stream:
            stats = Stats(pr, stream=stream)
            stats.strip_dirs()
            stats.sort_stats('time')
            stats.dump_stats('square.prof')
            stats.print_stats()
    else:
        model.run_model()