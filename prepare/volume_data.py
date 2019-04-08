from itertools import product
from os import path
from samri.report.snr import df_threshold_volume ,iter_threshold_volume
import nibabel as nib
import numpy as np
import pandas as pd
from bids.grabbids import BIDSLayout
from bids.grabbids import BIDSValidator

scratch_dir = '~/.scratch/irsabi'

def bids_autograb(bids_dir):
	bids_dir = path.abspath(path.expanduser(bids_dir))
	validate = BIDSValidator()
	layout = BIDSLayout(bids_dir)
	df = layout.as_data_frame()

	# Unclear in current BIDS specification, we refer to BOLD/CBV as modalities and func/anat as types
	df = df.rename(columns={'modality': 'type', 'type': 'modality'})
	return df

base_df = bids_autograb('{}/bids_collapsed'.format(scratch_dir))
base_df = base_df.loc[~base_df['path'].str.endswith('.json')]
base_df = base_df.loc[base_df['modality'].isin(['bold','cbv'])]
base_df['uID'] = base_df['subject']+'_'+base_df['session']+'_'+base_df['modality']

generic_df = bids_autograb('{}/preprocessing/generic_collapsed'.format(scratch_dir))
generic_df = generic_df.loc[~generic_df['path'].str.endswith('.json')]
generic_df = generic_df.loc[generic_df['modality'].isin(['bold','cbv'])]
generic_df['uID'] = generic_df['subject']+'_'+generic_df['session']+'_'+generic_df['modality']

generic_ambmc_df = bids_autograb('{}/preprocessing/generic_ambmc_collapsed'.format(scratch_dir))
generic_ambmc_df = generic_ambmc_df.loc[~generic_ambmc_df['path'].str.endswith('.json')]
generic_ambmc_df = generic_ambmc_df.loc[generic_ambmc_df['modality'].isin(['bold','cbv'])]
generic_ambmc_df['uID'] = generic_ambmc_df['subject']+'_'+generic_ambmc_df['session']+'_'+generic_ambmc_df['modality']

legacy_df = bids_autograb('{}/preprocessing/legacy_collapsed'.format(scratch_dir))
legacy_df = legacy_df.loc[~legacy_df['path'].str.endswith('.json')]
legacy_df = legacy_df.loc[legacy_df['modality'].isin(['bold','cbv'])]
legacy_df['uID'] = legacy_df['subject']+'_'+legacy_df['session']+'_'+legacy_df['modality']

legacy_dsurqec_df = bids_autograb('{}/preprocessing/legacy_dsurqec_collapsed'.format(scratch_dir))
legacy_dsurqec_df = legacy_dsurqec_df.loc[~legacy_dsurqec_df['path'].str.endswith('.json')]
legacy_dsurqec_df = legacy_dsurqec_df.loc[legacy_dsurqec_df['modality'].isin(['bold','cbv'])]
legacy_dsurqec_df['uID'] = legacy_dsurqec_df['subject']+'_'+legacy_dsurqec_df['session']+'_'+legacy_dsurqec_df['modality']

uids = base_df['uID'].unique()
generic_df = generic_df.loc[generic_df['uID'].isin(uids)]
legacy_df = legacy_df.loc[legacy_df['uID'].isin(uids)]

base_df['Processing'] = 'Unprocessed'
generic_df['Processing'] = 'Generic'
generic_ambmc_df['Processing'] = 'Generic'
legacy_df['Processing'] = 'Legacy'
legacy_dsurqec_df['Processing'] = 'Legacy'

base_df['Template'] = 'Unprocessed'
generic_df['Template'] = 'Generic'
generic_ambmc_df['Template'] = 'Legacy'
legacy_df['Template'] = 'Legacy'
legacy_dsurqec_df['Template'] = 'Generic'

base_df['Threshold'] = ''
generic_df['Threshold'] = ''
generic_ambmc_df['Threshold'] = ''
legacy_df['Threshold'] = ''
legacy_dsurqec_df['Threshold'] = ''
for uid in uids:
	img = nib.load(base_df.loc[base_df['uID'] == uid, 'path'].item())
	data = img.get_data()
	threshold = np.percentile(data,66)
	base_df.loc[base_df['uID'] == uid, 'Threshold'] = threshold
	generic_df.loc[generic_df['uID'] == uid, 'Threshold'] = threshold
	generic_ambmc_df.loc[generic_ambmc_df['uID'] == uid, 'Threshold'] = threshold
	legacy_df.loc[legacy_df['uID'] == uid, 'Threshold'] = threshold
	legacy_dsurqec_df.loc[legacy_dsurqec_df['uID'] == uid, 'Threshold'] = threshold

df = pd.DataFrame([])
df_ = df_threshold_volume(base_df,
	threshold='Threshold',
	)
df = df.append(df_)
df_ = df_threshold_volume(generic_df,
	threshold='Threshold',
	)
df = df.append(df_)
df_ = df_threshold_volume(generic_ambmc_df,
	threshold='Threshold',
	)
df = df.append(df_)
df_ = df_threshold_volume(legacy_df,
	threshold='Threshold',
	)
df_['Thresholded Volume'] = df_['Thresholded Volume']/1000.
df = df.append(df_)
df_ = df_threshold_volume(legacy_dsurqec_df,
	threshold='Threshold',
	)
df_['Thresholded Volume'] = df_['Thresholded Volume']/1000.
df = df.append(df_)

# Ar a voxel size of 0.2mm isotropic we are only sensitive to about 0.008mm^3
df = df.round({'Volume':3,'Thresholded Volume':3})

# Calculate Volume Conservation Factor
df['Volume Conservation Factor']=-1
uids = df['uID'].unique()
templates = [i for i in df['Template'].unique() if i != 'Unprocessed']
processings = [i for i in df['Processing'].unique() if i != 'Unprocessed']

for uid, template, processing in list(product(uids,templates,processings)):
	reference = df.loc[(df['uID']==uid) & (df['Processing']=='Unprocessed'), 'Thresholded Volume'].item()
	volume = df.loc[(df['uID']==uid) & (df['Processing']==processing) & (df['Template']==template), 'Thresholded Volume'].item()
	df.loc[(df['uID']==uid) & (df['Processing']==processing) & (df['Template']==template), 'Volume Conservation Factor'] = volume/reference

# Ready Strings for Printing
df['modality'] = df['modality'].str.upper()
df = df.rename(columns={'modality': 'Contrast',})
df.columns = map(str.title, df.columns)

df.to_csv('../data/volume.csv')
