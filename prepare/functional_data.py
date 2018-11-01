import pandas as pd

from samri.report.snr import df_significant_signal
from samri.utilities import bids_autofind_df, bids_autograb

masks = {
	'generic':'/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
	'generic_ambmc':'/usr/share/mouse-brain-atlases/ambmc_200micron_mask.nii.gz',
	'legacy':'/usr/share/mouse-brain-atlases/lambmc_200micron_mask.nii.gz',
	'legacy_dsurqec':'/usr/share/mouse-brain-atlases/ldsurqec_200micron_mask.nii.gz',
	}

df = pd.DataFrame([])
for key in masks:
	in_df = bids_autofind_df('~/ni_data/ofM.dr/l1/{}/'.format(key),
		path_template='sub-{{subject}}/ses-{{session}}/'\
			'sub-{{subject}}_ses-{{session}}_task-{{task}}_acq-{{acquisition}}_run-{{run}}_{{modality}}_pfstat.nii.gz',
		match_regex='.+sub-(?P<sub>.+)/ses-(?P<ses>.+)/'\
			'.*?_task-(?P<task>.+)_acq-(?P<acquisition>.+)_run-(?P<run>.+)_(?P<modality>cbv|bold)_pfstat\.nii.gz',
		)
	df_ = df_significant_signal(in_df,
		mask_path=masks[key],
		)
	if 'generic' in key:
		df_['Processing'] = 'Generic'
	else:
		df_['Processing'] = 'Legacy'
	if key in ['generic', 'legacy_dsurqec']:
		df_['Template'] = 'Generic'
	elif key in ['legacy', 'generic_ambmc']:
		df_['Template'] = 'Legacy'
	df = df.append(df_)

# Ready Strings for Printing
df['modality'] = df['modality'].str.upper()
df = df.rename(columns={'modality': 'Contrast',})
df.columns = map(str.title, df.columns)

df.to_csv('../data/functional.csv')
