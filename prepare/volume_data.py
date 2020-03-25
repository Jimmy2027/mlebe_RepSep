from itertools import product
from os import path
from samri.report.snr import df_threshold_volume ,iter_threshold_volume
import nibabel as nib
import numpy as np
import pandas as pd
from bids.grabbids import BIDSLayout
from bids.grabbids import BIDSValidator

scratch_dir = '~/.scratch/mlebe'

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

generic_masked_df = bids_autograb('{}/preprocessing/generic_masked_collapsed'.format(scratch_dir))
generic_masked_df = generic_masked_df.loc[~generic_masked_df['path'].str.endswith('.json')]
generic_masked_df = generic_masked_df.loc[generic_masked_df['modality'].isin(['bold','cbv'])]
generic_masked_df['uID'] = generic_masked_df['subject']+'_'+generic_masked_df['session']+'_'+generic_masked_df['modality']

uids = base_df['uID'].unique()
generic_df = generic_df.loc[generic_df['uID'].isin(uids)]
generic_masked_df = generic_masked_df.loc[generic_masked_df['uID'].isin(uids)]


base_df['Processing'] = 'Unprocessed'
generic_df['Processing'] = 'Generic'
generic_masked_df['Processing'] = 'Generic Masked'

base_df['Threshold'] = ''
generic_df['Threshold'] = ''
generic_masked_df['Threshold'] = ''

for uid in uids:
	img = nib.load(base_df.loc[base_df['uID'] == uid, 'path'].item())
	data = img.get_data()
	threshold = np.percentile(data,66)
	base_df.loc[base_df['uID'] == uid, 'Threshold'] = threshold
	generic_df.loc[generic_df['uID'] == uid, 'Threshold'] = threshold
	generic_masked_df.loc[generic_masked_df['uID'] == uid, 'Threshold'] = threshold


df = pd.DataFrame([])
df_ = df_threshold_volume(base_df,
	threshold='Threshold',
	)
df = df.append(df_)
df_ = df_threshold_volume(generic_df,
	threshold='Threshold',
	)
df = df.append(df_)
df_ = df_threshold_volume(generic_masked_df,
	threshold='Threshold',
	)
df = df.append(df_)

# Ar a voxel size of 0.2mm isotropic we are only sensitive to about 0.008mm^3
df = df.round({'Volume':3,'Thresholded Volume':3})

# Calculate Volume Conservation Factor
df['Volume Conservation Factor']=-1
df['1 - VCF']=-1
uids = df['uID'].unique()

processings = [i for i in df['Processing'].unique() if i != 'Unprocessed']
for uid, processing in list(product(uids,processings)):
	reference = df.loc[(df['uID']==uid) & (df['Processing']=='Unprocessed'), 'Thresholded Volume'].item()
	try:
		volume = df.loc[(df['uID']==uid) & (df['Processing']==processing), 'Thresholded Volume'].item()
	except:
		volume = 1
		print(uid, processing)
	df.loc[(df['uID']==uid) & (df['Processing']==processing), 'Volume Conservation Factor'] = volume/reference
	df.loc[(df['uID'] == uid) & (df['Processing'] == processing), '1 - VCF'] = np.abs(1 - volume / reference)

# Ready Strings for Printing
df['modality'] = df['modality'].str.upper()
df = df.rename(columns={'modality': 'Contrast',})
df.columns = map(str.title, df.columns)

df.to_csv(path.join(scratch_dir, 'data', 'volume.csv'))

"""
Bootstrapping
"""

volume_df = df
generic_df = volume_df.loc[volume_df['Processing']=='Generic']
generic_CBV_df = generic_df.loc[generic_df['Contrast']=='CBV']
generic_BOLD_df = generic_df.loc[generic_df['Contrast']=='BOLD']
generic_masked_df = volume_df.loc[volume_df['Processing']=='Generic Masked']
generic_masked_CBV_df = generic_masked_df.loc[generic_masked_df['Contrast']=='CBV']
generic_masked_BOLD_df = generic_masked_df.loc[generic_masked_df['Contrast']=='BOLD']


bootstrapped_RMSEs = pd.DataFrame(columns=['Contrast', 'Processing', 'Uid', 'RMSE'])

N = 10000

for i in range(N):
	generic_CBV_df_temp = choice(generic_CBV_df['Volume Conservation Factor'].to_list(), len(generic_CBV_df['Volume Conservation Factor'].to_list()))
	generic_BOLD_df_temp = choice(generic_BOLD_df['Volume Conservation Factor'].to_list(), len(generic_BOLD_df['Volume Conservation Factor'].to_list()))
	generic_masked_CBV_df_temp = choice(generic_masked_CBV_df['Volume Conservation Factor'].to_list(), len(generic_masked_CBV_df['Volume Conservation Factor'].to_list()))
	generic_masked_BOLD_df_temp = choice(generic_masked_BOLD_df['Volume Conservation Factor'].to_list(), len(generic_masked_BOLD_df['Volume Conservation Factor'].to_list()))
	rmse_generic_masked_CBV = sqrt(mean_squared_error([1] * len(generic_masked_CBV_df_temp), generic_masked_CBV_df_temp))
	rmse_generic_masked_BOLD = sqrt(mean_squared_error([1] * len(generic_masked_BOLD_df_temp), generic_masked_BOLD_df_temp))
	rmse_generic_CBV = sqrt(mean_squared_error([1] * len(generic_CBV_df_temp), generic_CBV_df_temp))
	rmse_generic_BOLD = sqrt(mean_squared_error([1] * len(generic_BOLD_df_temp), generic_BOLD_df_temp))
	bootstrapped_RMSEs =bootstrapped_RMSEs.append(pd.DataFrame([['CBV', 'Generic', '{}.1'.format(i), rmse_generic_CBV]], columns=['Contrast', 'Processing', 'Uid', 'RMSE']))
	bootstrapped_RMSEs =bootstrapped_RMSEs.append(pd.DataFrame([['BOLD', 'Generic', '{}.2'.format(i), rmse_generic_BOLD]], columns=['Contrast', 'Processing', 'Uid', 'RMSE']))
	bootstrapped_RMSEs =bootstrapped_RMSEs.append(pd.DataFrame([['CBV', 'Generic Masked', '{}.1'.format(i), rmse_generic_masked_CBV]], columns=['Contrast', 'Processing', 'Uid', 'RMSE']))
	bootstrapped_RMSEs =bootstrapped_RMSEs.append(pd.DataFrame([['BOLD', 'Generic Masked', '{}.2'.format(i), rmse_generic_masked_BOLD]], columns=['Contrast', 'Processing', 'Uid', 'RMSE']))

bootstrapped_RMSEs.to_csv('../data/bootstrapped_volume.csv')