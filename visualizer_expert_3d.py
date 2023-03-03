import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import struct
import numpy as np
import argparse
import math

import data_loader_r3d

def main(args):
    # visualize obstacles as rectangles
    size = 5
    obc = data_loader_r3d.load_obs_list(args.env_id, folder=args.data_path)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for (x, y, z) in obc:
        box = np.ones((x,y,z), dtype=np.bool)
        ax.voxels(box, facecolors='gray')

    for path_file in args.path_file:
        # visualize path
        if path_file.endswith('.txt'):
            path = np.loadtxt(path_file)
        else:
            path = np.fromfile(path_file)
        print(path)
        path = path.reshape(-1, 2)
        path_x = []
        path_y = []
        path_z = []

        for i in range(len(path)):
            path_x.append(path[i][0])
            path_y.append(path[i][1])
            path_z.append(path[i][2])

        plt.plot(path_x, path_y, marker='o')

        ax.plot(path_x, path_y,path_z)

        totdist = 0

        for i in range(len(path)-1):
            totdist += math.dist(path[i], path[i+1])

        print(path_file, " : ", totdist)

    plt.show()

parser = argparse.ArgumentParser()
parser.add_argument('--data-path', type=str, default='./data/')
parser.add_argument('--env-id', type=int, default=0)
parser.add_argument('--point-cloud', default=False, action='store_true')
parser.add_argument('--path-file', nargs='*', type=str, default=["./data/e0/path1001.dat"], help='path file')
args = parser.parse_args()
print(args)
main(args)
