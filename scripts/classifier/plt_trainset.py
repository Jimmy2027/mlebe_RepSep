import numpy as np
import random
from matplotlib import pyplot as plt
import os

seed = 1
x_train = np.load(os.path.expanduser('~/.scratch/mlebe_+bc_+btr/classifiers/T2/x_train_augmented.npy'))
y_train = np.load(os.path.expanduser('~/.scratch/mlebe_+bc_+btr/classifiers/T2/y_train_augmented.npy'))
np.random.seed(seed)
np.random.shuffle(x_train)
np.random.seed(seed)
np.random.shuffle(y_train)


for idx, i in enumerate(range(8)):
    plt.subplot(2, 4, idx+1)
    plt.imshow(np.squeeze(x_train[i]), cmap='gray')
    plt.imshow(np.squeeze(y_train[i]), alpha=0.6, cmap='Blues')
    plt.axis('off')
