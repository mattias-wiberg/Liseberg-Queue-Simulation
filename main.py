import random
from model import Model
import numpy as np
import cProfile
from pstats import Stats, SortKey
import multiprocessing as mp
np.random.seed(10)
random.seed(10)

def fun(model):
    model.run_model()

if __name__ == '__main__':
    models = [Model(0.001), Model(0.1), Model(0.01)]

    do_profiling = False
    if do_profiling:
        with cProfile.Profile() as pr:
            with mp.Pool(mp.cpu_count) as pool:
                pool.map_async(fun,models)

        with open('profiling_stats.txt', 'w') as stream:
            stats = Stats(pr, stream=stream)
            stats.strip_dirs()
            stats.sort_stats('time')
            stats.dump_stats('square.prof')
            stats.print_stats()
    else:
        models[0].run_model()