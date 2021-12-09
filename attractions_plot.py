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
        

#load_data("park_data.csv")
a = []
visit = [1,2,3,4,5]
print(a)
for to_visit in visit:
    if len(a) != 3:
        a.append(to_visit)
    else:
        a.remove(a[0])
        a.append(to_visit)
    
    print(a)