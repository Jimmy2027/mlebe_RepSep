import os

import numpy as np
from matplotlib import pyplot as plt
from mlebe.training.configs.utils import json_to_dict

seed = 2
config_path = os.path.expanduser('data/config.json')
config = json_to_dict(config_path)
path = 'data/classifier'
nbr_images = 13

x_test = np.load(path + '/x_test.npy', allow_pickle=True)
y_test = np.load(path + '/y_test.npy', allow_pickle=True)
y_pred = np.load(path + '/y_pred.npy', allow_pickle=True)
np.random.seed(seed)
np.random.shuffle(x_test)
np.random.seed(seed)
np.random.shuffle(y_test)
np.random.seed(seed)
np.random.shuffle(y_pred)

list = [[x_test[:nbr_images]], [y_test[:nbr_images]], [y_pred[:nbr_images]]]

for img in range(len(list[0])):
    patches = []
    for l in range(len(list)):
        patch = list[l][img][0] * 255
        for slice in range(1, list[l][img].shape[0]):
            temp = list[l][img][slice] * 255
            patch = np.hstack((patch, temp))
        patches.append(patch)
    patch = patches[0]
    for i in range(1, len(patches)):
        patch = np.vstack((patch, patches[i]))
    image = np.vstack(patches)
    plt.figure()
    plt.imshow(image, cmap='gray')
    plt.axis('off')
