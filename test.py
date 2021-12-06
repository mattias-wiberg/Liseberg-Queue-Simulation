import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation

names = []
def load_data(path):
    data = np.genfromtxt(path, delimiter=',', dtype=("U20",float,float,int,int,int))
    
    R = 6371000 # World radius
    origin = data[0]
    lat = origin[1]
    lon = origin[2]
    org_x = R * np.cos(np.deg2rad(lat)) * np.cos(np.deg2rad(lon))
    org_y = R * np.cos(np.deg2rad(lat)) * np.sin(np.deg2rad(lon))

    for row in data[0:]:
        name = row[0]
        lat = row[1]
        lon = row[2]
        x = R * np.cos(np.deg2rad(lat)) * np.cos(np.deg2rad(lon))
        y = R * np.cos(np.deg2rad(lat)) * np.sin(np.deg2rad(lon))
        names.append(name)
        x,y = np.array([[0, 1],[-1, 0]]).dot([x-org_x,y-org_y])
        plt.scatter(x, y)
    plt.axis('equal')
    plt.grid(False)
    plt.legend(names)
    plt.show()
        


#
fig, ax = plt.subplots()    

data = np.cumsum(np.random.normal(size=100)) #some list of data

ax.grid()

def plot(a, data):
    data += np.cumsum(np.random.normal(size=100)+3e-2)
    X = np.c_[data[::2], data[1::2]]
    ax.clear()
    sc = ax.scatter(data[::2], data[1::2], c=data[1::2], s=data[1::2])
    #sc.set_offsets(X)
    # manually relim:
    xmin=X[:,0].min(); xmax=X[:,0].max()
    ymin=X[:,1].min(); ymax=X[:,1].max()
    ax.set_xlim(xmin-0.1*(xmax-xmin),xmax+0.1*(xmax-xmin))
    ax.set_ylim(ymin-0.1*(ymax-ymin),ymax+0.1*(ymax-ymin))

#ani = matplotlib.animation.FuncAnimation(fig, plot, fargs=(data,),
#            frames=4, interval=100, repeat=True) 
#plt.show()


load_data("attraction_data.csv")

#%%
import glob
from PIL import Image

# filepaths
fp_in = "./save/*.png"
fp_out = "./image.gif"

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
img, *imgs = [Image.open(f) for f in glob.glob(fp_in).sort(key = int)]
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=2, loop=0)

# %%
