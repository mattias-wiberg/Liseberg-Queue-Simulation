import random
from model import Model
import numpy as np
import cProfile
from pstats import Stats, SortKey
from agent import Type
np.random.seed(10)
random.seed(10)

if __name__ == '__main__':
    #model = Model(mix=[(Type.RANDOM, 0.5),(Type.SMART, 0.5)])
    model = Model(target_n_agents=1000, draw=True)

    do_profiling = False
    if do_profiling:
        with cProfile.Profile() as pr:
            model.run()

        with open('profiling_stats.txt', 'w') as stream:
            stats = Stats(pr, stream=stream)
            stats.strip_dirs()
            stats.sort_stats('time')
            stats.dump_stats('square.prof')
            stats.print_stats()
    else:
        model.run()