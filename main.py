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
	delays = [0]#[0, 30, 60, 5*60, 10*60, 20*60, 30*60, 40*60, 60*60]
	mix = [(Type.SMART, 1)]
	for delay in delays:
		model = Model(mix,delay)

		do_profiling = False
		if do_profiling:
			with cProfile.Profile() as pr:
				model.run(2000)

			with open('profiling_stats.txt', 'w') as stream:
				stats = Stats(pr, stream=stream)
				stats.strip_dirs()
				stats.sort_stats('time')
				stats.dump_stats('square.prof')
				stats.print_stats()
		else:
			#43200 = 12 hours
			model.run(43200, draw=True, interactive=False, draw_export=True, save=False, draw_interval=10)
