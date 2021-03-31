import pandas as pd
from matplotlib import pyplot as plt
import os
import nibabel as nib

template_dir = "/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii"
blacklist_selection = pd.read_csv('data/Blacklist/blacklist.csv')

indexes = [3, 5, 5, 7, 8, 8, 8, 15]
slices = [73, 23, 63, 16, 22, 62, 75, 23]
plt.figure()
counter = 1
for index, s in zip(indexes, slices):
    plt.subplot(2, 4, counter)
    img = nib.load(blacklist_selection.iloc[index]['path']).get_data()
    target = nib.load(template_dir).get_data()
    plt.imshow(img[:, s, :], cmap='gray')
    plt.imshow(target[:, s, :], cmap='Blues', alpha=0.6)
    plt.axis('off')
    counter += 1

plt.show()
