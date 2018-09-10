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

legacy_df = bids_autograb('~/ni_data/ofM.dr/preprocessing/legacy_collapsed')
legacy_df = legacy_df.loc[~legacy_df['path'].str.endswith('.json')]
legacy_df = legacy_df.loc[legacy_df['type'].isin(['bold','cbv'])]
legacy_df['uID'] = legacy_df['subject']+'_'+legacy_df['session']+'_'+legacy_df['type']

uids = base_df['uID'].unique()
generic_df = generic_df.loc[generic_df['uID'].isin(uids)]
legacy_df = legacy_df.loc[legacy_df['uID'].isin(uids)]

base_df['Processing'] = 'Unprocessed'
generic_df['Processing'] = 'Generic'
legacy_df['Processing'] = 'Legacy'

base_df['threshold'] = ''
base_files = base_df['path'].tolist()
for base_file in base_files:
	img = nib.load(base_file)
	data = img.get_data()
	threshold = np.percentile(data,50)
	base_df.loc[base_df['path'] == base_file, 'threshold'] = threshold
	generic_df.loc[generic_df['path'] == base_file, 'threshold'] = threshold
	legacy_df.loc[legacy_df['path'] == base_file, 'threshold'] = threshold

df = pd.DataFrame([])
df_ = df_threshold_volume(base_df,
	threshold='threshold',
	)
df = df.append(df_)
df_ = df_threshold_volume(generic_df,
	threshold='threshold',
	)
df = df.append(df_)
df_ = df_threshold_volume(legacy_df,
	threshold='threshold',
	)
df_['thresholded volume'] = df_['thresholded volume']/1000.
df = df.append(df_)
df.to_csv('../data/volumes.csv')
