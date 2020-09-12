"""
This script plots all the registered irsabi volumes, slice by slice with in each plot one slice of the generic workflow anf one of the masked to compare them.
"""
import os
import nibabel as nib
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm
import pandas as pd

preprocessed_folders = [os.path.expanduser('~/.scratch/mlebe_threed/preprocessing/generic'),
                        os.path.expanduser('~/.scratch/mlebe_threed/preprocessing/masked')]
template_path = '/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii'

table = pd.DataFrame(columns=['generic_volume_path', 'masked_volume_path', 'folder_name'])

for preprocessed_folder in preprocessed_folders:
    for root, dirs, files in os.walk(preprocessed_folder):
        for file in files:
            if file.endswith('T2w.nii.gz'):
                file_path = '/'.join([root, file])
                if 'generic' in file_path:
                    table = table.append({'generic_volume_path': file_path, 'folder_name': file.split('.')[0]},
                                         ignore_index=True)
                elif 'masked' in file_path:
                    table.loc[table['folder_name'] == file.split('.')[0], 'masked_volume_path'] = file_path

template = nib.load(template_path).get_data()

for idx in tqdm(range(len(table))):
    row = table.iloc[idx]
    generic_volume = nib.load(row['generic_volume_path']).get_data()
    masked_volume = nib.load(row['masked_volume_path']).get_data()
    folder_name = os.path.join('temp', row['folder_name'])
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    f = open(os.path.join(folder_name, "path.txt"), "w")
    f.write(row['generic_volume_path'] + '\n\n' + row['masked_volume_path'])
    f.close()
    for i in range(template.shape[1]):
        if np.max(template[:, i, :]):
            print(folder_name + '/{}'.format(i))
            plt.figure()
            plt.subplot(1, 2, 1)
            plt.imshow(generic_volume[:, i, :], cmap='gray')
            plt.imshow(template[:, i, :], alpha=0.3, cmap='Blues')
            plt.title('Generic')
            plt.axis('off')
            plt.subplot(1, 2, 2)
            plt.imshow(masked_volume[:, i, :], cmap='gray')
            plt.imshow(template[:, i, :], alpha=0.3, cmap='Blues')
            plt.title('Masked')
            plt.axis('off')
            plt.savefig(folder_name + '/{}'.format(i))
            plt.close()
