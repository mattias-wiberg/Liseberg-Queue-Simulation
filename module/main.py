from pickle import FALSE
import random
from model import Model
import numpy as np
import cProfile
from pstats import Stats, SortKey
from agent import Type
import sys
import os
np.random.seed(10)
random.seed(10)

REMOTE = False

if __name__ == '__main__':
    #model = Model(mix=[(Type.RANDOM, 0.5),(Type.SMART, 0.5)])
    # [0, 30, 60, 5*60, 10*60, 20*60, 30*60, 40*60, 60*60]
    delay = int(sys.argv[1])
    mix_arg = sys.argv[2:]
    mix = []
    for i in range(0, len(mix_arg), 2):
        mix.append((Type.__getitem__(mix_arg[i]
                                     ), float(mix_arg[i+1])))
    model = Model(mix, delay)

    do_profiling = False
    if do_profiling:
        with cProfile.Profile() as pr:
            model.run(2000)

        with open('../profile/profiling_stats.txt', 'w') as stream:
            stats = Stats(pr, stream=stream)
            stats.strip_dirs()
            stats.sort_stats('time')
            stats.dump_stats('square.prof')
            stats.print_stats()
    else:
        # Make logs folder
        types, probs = list(zip(*mix))
        folder_name = ""
        for i in range(len(types)):
            folder_name += types[i].name + "_" + str(probs[i])
            if i != len(types)-1:
                folder_name += "-"
        logs_path = "Z:/" if REMOTE else ".."
        logs_path += "/logs/"+folder_name+"/"+str(delay)
        os.makedirs(logs_path, exist_ok=True)
        # 43200 = 12 hours
        model.run(43200, logs_path)
