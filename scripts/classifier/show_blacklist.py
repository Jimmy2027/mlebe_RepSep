import pickle
from matplotlib import pyplot as plt
import numpy as np

xfile = open('/home/hendrik/.scratch/mlebe/classifier/blacklisted_images.pkl', 'rb')
blacklisted_images = pickle.load(xfile)
xfile.close()
yfile = open('/home/hendrik/.scratch/mlebe/classifier/blacklisted_masks.pkl', 'rb')
blacklisted_masks = pickle.load(yfile)
yfile.close()
plt.figure()
for idx, i in enumerate(range(114, 122)):
    plt.subplot(2, 4, idx+1)
    plt.imshow(np.squeeze(blacklisted_images[i]), cmap='gray')
    plt.imshow(np.squeeze(blacklisted_masks[i]), alpha=0.6, cmap='Blues')
    plt.axis('off')


