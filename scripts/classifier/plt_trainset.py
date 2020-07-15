import numpy as np
from matplotlib import pyplot as plt
import os

seed = 10
x_train = np.load('data/classifiers/T2/x_train.npy', allow_pickle=True)
y_train = np.load('data/classifiers/T2/y_train.npy', allow_pickle=True)
np.random.seed(seed)
np.random.shuffle(x_train)
np.random.seed(seed)
np.random.shuffle(y_train)


for idx, i in enumerate(range(8)):
    plt.subplot(2, 4, idx+1)
    plt.imshow(np.squeeze(x_train[i]), cmap='gray')
    plt.imshow(np.squeeze(y_train[i]), alpha=0.1, cmap='Blues')
    plt.axis('off')
