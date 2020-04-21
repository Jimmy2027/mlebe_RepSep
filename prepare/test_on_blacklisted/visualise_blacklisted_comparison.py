import os
from subjects_reader import find_subjects
from samri.pipelines.utils import bids_data_selection
from bids.grabbids import BIDSLayout
from bids.grabbids import BIDSValidator
import pandas as pd
from copy import deepcopy
from samri.pipelines.utils import filter_data
import nibabel as nib
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

registration_mask = '/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii'
blacklist_df = pd.read_csv(os.path.expanduser('~/Desktop/MLEBE/mlebe/Blacklist/blacklist.csv'))
print(blacklist_df.head())
dir = os.path.expanduser('../data/blacklist_comparison/')

blacklist_df = blacklist_df.loc[blacklist_df['label'] == 'bad']
print(blacklist_df.head())
# counts_df = blacklist_df.groupby(['study', 'subject', 'session', 'acquisition', 'modality']).count()
# scan = pd.DataFrame([counts_df.loc[counts_df['slice'] == counts_df['slice'].max()].index.values[0]], columns=['study', 'subject', 'session', 'acquisition', 'modality'])
# print(blacklist_df['subject'], scan['subject'].item())

# print(slices)

for o in os.listdir(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('T2w.nii.gz'):
                subject = file.split('_')[0].split('-')[1]
                acquisition = file.split('_')[2].split('-')[1]
                session = file.split('_')[1].split('-')[1]
                if o == 'generic':
                    generic_scan = os.path.join(root, file)
                    print(root, file)
                if o == 'masked':
                    mlebe_scan = os.path.join(root, file)

mask = np.moveaxis(nib.load(registration_mask).get_data(),2,0)
generic_scan = np.moveaxis(nib.load(generic_scan).get_data(),2,0)
mlebe_scan = np.moveaxis(nib.load(mlebe_scan).get_data(),2,0)

slices = blacklist_df.loc[(blacklist_df['subject'] == int(subject)) & (blacklist_df['acquisition'] == acquisition) & (blacklist_df['session'] == session)]['slice'].values.tolist()
print(blacklist_df.loc[(blacklist_df['subject'] == int(subject))])
print(generic_scan.shape)
for i in range(mlebe_scan.shape[0]):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(mlebe_scan[i], cmap='gray')
    ax1.imshow(mask[i], alpha=0.4, cmap='Blues')
    ax1.set_title('masked')
    ax2.imshow(generic_scan[i], cmap='gray')
    ax2.imshow(mask[i], alpha=0.4, cmap='Blues')
    ax2.set_title('generic')
    plt.savefig(os.path.join(dir, 'temp','slice_{}'.format(i)))




# bids_dir = os.path.expanduser('~/.scratch/mlebe_backlist/bids')
#
# functional_match = {'acquisition': ['EPI'], }
# structural_match = {'acquisition': ['TurboRARE'], }
# subjects = find_subjects(bids_dir)
# print(subjects)
# data_selection_generic = bids_data_selection(os.path.join(dir, 'generic'), structural_match, functional_match, subjects, sessions=[])
# data_selection_generic = data_selection_generic.loc[data_selection_generic['type'] == 'anat']
# data_selection_masked = bids_data_selection(os.path.join(dir, 'generic_masked'), structural_match, functional_match, subjects, sessions=[])
# data_selection_masked = data_selection_masked.loc[data_selection_masked['type'] == 'anat']
# data_selection_masked.to_csv(bids_dir + '/masked_data_sel.csv')
#
# for masked_path in data_selection_masked['path'].values.tolist():
#     masked_image = np.moveaxis(nib.load(masked_path).get_data(), 2, 0)
#     subject = data_selection_masked.loc[data_selection_masked['path'] == masked_path, 'subject'].item()
#     session = data_selection_masked.loc[data_selection_masked['path'] == masked_path, 'session'].item()
#     generic_path = data_selection_generic.loc[(data_selection_generic['subject'] == subject) & (data_selection_generic['session'] == session), 'path'].item()
#     generic_image = np.moveaxis(nib.load(generic_path).get_data(), 2, 0)
#     os.makedirs(os.path.join(dir,'temp', subject + session), exist_ok= True)
