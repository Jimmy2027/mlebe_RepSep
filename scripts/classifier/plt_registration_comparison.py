import os
import pandas as pd
from matplotlib import pyplot as plt
import nibabel as nib

table = pd.DataFrame(
    [['sub-4005_ses-ofMaF_acq-TurboRARElowcov_T2w', 61], ['sub-4001_ses-ofMcF2_acq-TurboRARElowcov_T2w', 42],
     ['sub-4001_ses-ofMcF2_acq-TurboRARElowcov_T2w', 33]], columns=['volume', 'slice'], index=[1, 2, 3])

preprocessed_folders = [os.path.expanduser('~/.scratch/mlebe/preprocessing/generic'),
                        os.path.expanduser('~/.scratch/mlebe/preprocessing/masked')]
template_path = '/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii'
template_volume = nib.load(template_path).get_data()

generic_preprocessed_list = []
masked_preprocessed_list = []

for preprocessed_folder in preprocessed_folders:
    for root, dirs, files in os.walk(preprocessed_folder):
        for file in files:
            if file.split('.')[0] in table['volume'].to_list():
                file_path = '/'.join([root, file])
                subject = file.split('_')[0]
                if 'generic' in file_path:
                    table.loc[table['volume'] == file.split('.')[0], 'generic_path'] = file_path
                elif 'masked' in file_path:
                    table.loc[table['volume'] == file.split('.')[0], 'masked_path'] = file_path

fig, axs = plt.subplots(nrows=2, ncols=4,
                        subplot_kw={'xticks': [], 'yticks': []})

for idx, ax in enumerate(axs.flat[:4]):
    if idx == 0:
        ax.text(0.5, 0.5, 'Generic', size=15, ha='center', va='center')
        ax.axis("off")
    else:
        volume = nib.load(table.iloc[idx - 1]['generic_path']).get_data()
        ax.imshow(volume[:, table.iloc[idx - 1]['slice'], :], cmap='gray')
        ax.imshow(template_volume[:, table.iloc[idx - 1]['slice'], :], alpha=0.7, cmap='Blues')
for idx, ax in enumerate(axs.flat[4:]):
    if idx == 0:
        ax.text(0.5, 0.5, 'Masked', size=15, ha='center', va='center')
        ax.axis("off")
    else:
        volume = nib.load(table.iloc[idx - 1]['masked_path']).get_data()
        ax.imshow(volume[:, table.iloc[idx - 1]['slice'], :], cmap='gray')
        ax.imshow(template_volume[:, table.iloc[idx - 1]['slice'], :], alpha=0.7, cmap='Blues')

plt.show()
