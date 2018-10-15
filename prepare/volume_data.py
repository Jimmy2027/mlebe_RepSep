from samri.report.snr import df_threshold_volume ,iter_threshold_volume
from samri.utilities import bids_autograb
import nibabel as nib
import numpy as np
import pandas as pd

base_df = bids_autograb('~/ni_data/ofM.dr/bids_collapsed')
base_df = base_df.loc[~base_df['path'].str.endswith('.json')]
base_df = base_df.loc[base_df['type'].isin(['bold','cbv'])]
base_df['uID'] = base_df['subject']+'_'+base_df['session']+'_'+base_df['type']

generic_df = bids_autograb('~/ni_data/ofM.dr/preprocessing/generic_collapsed')
generic_df = generic_df.loc[~generic_df['path'].str.endswith('.json')]
generic_df = generic_df.loc[generic_df['type'].isin(['bold','cbv'])]
generic_df['uID'] = generic_df['subject']+'_'+generic_df['session']+'_'+generic_df['type']

generic_ambmc_df = bids_autograb('~/ni_data/ofM.dr/preprocessing/generic_ambmc_collapsed')
generic_ambmc_df = generic_ambmc_df.loc[~generic_ambmc_df['path'].str.endswith('.json')]
generic_ambmc_df = generic_ambmc_df.loc[generic_ambmc_df['type'].isin(['bold','cbv'])]
generic_ambmc_df['uID'] = generic_ambmc_df['subject']+'_'+generic_ambmc_df['session']+'_'+generic_ambmc_df['type']

legacy_df = bids_autograb('~/ni_data/ofM.dr/preprocessing/legacy_collapsed')
legacy_df = legacy_df.loc[~legacy_df['path'].str.endswith('.json')]
legacy_df = legacy_df.loc[legacy_df['type'].isin(['bold','cbv'])]
legacy_df['uID'] = legacy_df['subject']+'_'+legacy_df['session']+'_'+legacy_df['type']

legacy_dsurqec_df = bids_autograb('~/ni_data/ofM.dr/preprocessing/legacy_dsurqec_collapsed')
legacy_dsurqec_df = legacy_dsurqec_df.loc[~legacy_dsurqec_df['path'].str.endswith('.json')]
legacy_dsurqec_df = legacy_dsurqec_df.loc[legacy_dsurqec_df['type'].isin(['bold','cbv'])]
legacy_dsurqec_df['uID'] = legacy_dsurqec_df['subject']+'_'+legacy_dsurqec_df['session']+'_'+legacy_dsurqec_df['type']

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

df.to_csv('../data/volumes.csv')
