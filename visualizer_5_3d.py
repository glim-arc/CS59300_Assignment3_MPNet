import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import struct
import numpy as np
import argparse
import math
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt

import data_loader_r3d

def cuboid_data2(o, size=(1,1,1)):
    X = [[[0, 1, 0], [0, 0, 0], [1, 0, 0], [1, 1, 0]],
         [[0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0]],
         [[1, 0, 1], [1, 0, 0], [1, 1, 0], [1, 1, 1]],
         [[0, 0, 1], [0, 0, 0], [0, 1, 0], [0, 1, 1]],
         [[0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 0]],
         [[0, 1, 1], [0, 0, 1], [1, 0, 1], [1, 1, 1]]]
    X = np.array(X).astype(float)
    for i in range(3):
        X[:,:,i] *= size[i]
    X += np.array(o)
    return X

def plotCubeAt2(positions,sizes=None,colors=None, **kwargs):
    if not isinstance(colors,(list,np.ndarray)): colors=["C0"]*len(positions)
    if not isinstance(sizes,(list,np.ndarray)): sizes=[(1,1,1)]*len(positions)
    g = []
    for p,s,c in zip(positions,sizes,colors):
        g.append( cuboid_data2(p, size=s) )
    return Poly3DCollection(np.concatenate(g),
                            facecolors=np.repeat(colors,6), **kwargs)

def main(args):

    if args.point_cloud:
        # visualize obstacles as point cloud
        file = args.data_path + f'obs_cloud/obc{args.env_id}.dat'
        obs = []
        temp = np.fromfile(file)
        obs.append(temp)
        obs = np.array(obs).astype(np.float32).reshape(-1, 3)
        ax.scatter3D(obs[:, 0], obs[:, 1], obs[:, 2], cmap='blue')
    else:
        obc = data_loader_r3d.load_obs_list(args.env_id, folder=args.data_path)

        cubesize = [[5, 5, 10], [5, 10, 5], [5, 10, 10], [10, 5, 5], [10, 5, 10], [10, 10, 5], [10, 10, 10], [5, 5, 5],
                    [10, 10, 10], [5, 5, 5]]

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        ax.set_xlim(-30, 30)
        ax.set_ylim(-30, 30)
        ax.set_zlim(-30, 30)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        colors = ["red"]*len(cubesize)

        ax.add_collection3d(plotCubeAt2(obc, cubesize,colors=colors, edgecolor="k"))

    for path_file in args.path_file:
            # visualize path
            if path_file.endswith('.txt'):
                path = np.loadtxt(path_file)
            else:
                path = np.fromfile(path_file)
            print(path)
            path = path.reshape(-1, 3)
            path_x = []
            path_y = []
            path_z = []

            for i in range(len(path)):
                path_x.append(path[i][0])
                path_y.append(path[i][1])
                path_z.append(path[i][2])

            ax.plot3D(path_x, path_y,path_z, marker='o')

            totdist = 0

            for i in range(len(path)-1):
                totdist += math.dist(path[i], path[i+1])

            print(path_file, " : ", totdist)

    plt.show()

parser = argparse.ArgumentParser()
parser.add_argument('--data-path', type=str, default='./data/')
parser.add_argument('--env-id', type=int, default=0)
parser.add_argument('--point-cloud', default=False, action='store_true')
parser.add_argument('--path-file', nargs='*', type=str, default=["./results2/env_0/path_4001_1.txt", "./results2/env_0/path_4001_2.txt", "./results2/env_0/path_4001_3.txt", "./results2/env_0/path_4001_4.txt", "./results2/env_0/path_4001_5.txt"], help='path file')
args = parser.parse_args()
print(args)
main(args)
