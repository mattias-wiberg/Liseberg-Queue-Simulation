
import os
import glob
import imageio

frames = []
files = glob.glob('./save/' + '*')
for filename in files:
	frames.append(imageio.imread(filename))
imageio.mimsave("flash_gif.gif", frames, format='GIF', fps=30)