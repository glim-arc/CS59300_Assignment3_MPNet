import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import struct
import numpy as np
import argparse

import data_loader_2d

def main(args):
    if args.point_cloud:
        # visualize obstacles as point cloud
        file = args.data_path + f'obs_cloud/obc{args.env_id}.dat'
        obs = []
        temp=np.fromfile(file)
        obs.append(temp)
        obs = np.array(obs).astype(np.float32).reshape(-1,2)
        plt.scatter(obs[:,0], obs[:,1], c='gray')
    else:
        # visualize obstacles as rectangles
        size = 5
        obc = data_loader_2d.load_obs_list(args.env_id, folder=args.data_path)
        for (x,y) in obc:
            r = mpatches.Rectangle((x-size/2,y-size/2),size,size,fill=True,color='gray')
            plt.gca().add_patch(r)

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
        for i in range(len(path)):
            path_x.append(path[i][0])
            path_y.append(path[i][1])

        plt.plot(path_x, path_y, marker='o')

    plt.show()


parser = argparse.ArgumentParser()
parser.add_argument('--data-path', type=str, default='./data/')
parser.add_argument('--env-id', type=int, default=0)
parser.add_argument('--point-cloud', default=False, action='store_true')
parser.add_argument('--path-file', nargs='*', type=str, default=["./results2/env_0/path_4001_1.txt", "./results2/env_0/path_4001_2.txt", "./results2/env_0/path_4001_3.txt", "./results2/env_0/path_4001_4.txt", "./results2/env_0/path_4001_5.txt"], help='path file')
args = parser.parse_args()
print(args)
main(args)
