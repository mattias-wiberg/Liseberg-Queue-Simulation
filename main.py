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
    model = Model(target_n_agents=12000,spawn_rules=[(1,0), (1, 80000)],mix=[(Type.NAIVE, 0.5), (Type.SMART, 0.5)], draw=False, draw_interval=10)

    do_profiling = False
    if do_profiling:
        with cProfile.Profile() as pr:
            model.run(10000)

        with open('profiling_stats.txt', 'w') as stream:
            stats = Stats(pr, stream=stream)
            stats.strip_dirs()
            stats.sort_stats('time')
            stats.dump_stats('square.prof')
            stats.print_stats()
    else:
        model.run(43200)