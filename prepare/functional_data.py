import pandas as pd

from samri.report.snr import df_significant_signal
from samri.report.utilities import df_roi_data
from samri.utilities import bids_autofind_df, bids_autograb

# Total significance
masks = {
	'generic':'/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
	'generic_ambmc':'/usr/share/mouse-brain-atlases/ambmc_200micron_mask.nii',
	'legacy':'/usr/share/mouse-brain-atlases/lambmc_200micron_mask.nii',
	'legacy_dsurqec':'/usr/share/mouse-brain-atlases/ldsurqec_200micron_mask.nii',
	}
masks_dr = {
	'generic':'/usr/share/mouse-brain-atlases/dsurqec_200micron_roi-dr.nii',
	'generic_ambmc':'/usr/share/mouse-brain-atlases/ambmc_200micron_roi-dr.nii',
	'legacy':'/usr/share/mouse-brain-atlases/lambmc_200micron_roi-dr.nii',
	'legacy_dsurqec':'/usr/share/mouse-brain-atlases/ldsurqec_200micron_roi-dr.nii',
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
		mask_path=masks_dr[key],
		column_string='DR Significance',
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

# Create processing and template-independent unique identifiers
df['uID'] = df['subject']+'_'+df['session']+'_'+df['modality']

# Ready Strings for Printing
df['modality'] = df['modality'].str.upper()
df.columns = map(str.title, df.columns)
df = df.rename(
	columns={
		'Mean Dr Significance':'Mean DR Significance',
		'Median Dr Significance':'Median DR Significance',
		'Modality':'Contrast',
		})

df.to_csv('../data/functional_significance.csv')

df = pd.DataFrame([])
for key in masks:
	in_df = bids_autofind_df('~/ni_data/ofM.dr/l1/{}/'.format(key),
		path_template='sub-{{subject}}/ses-{{session}}/'\
			'sub-{{subject}}_ses-{{session}}_task-{{task}}_acq-{{acquisition}}_run-{{run}}_{{modality}}_tstat.nii.gz',
		match_regex='.+sub-(?P<sub>.+)/ses-(?P<ses>.+)/'\
			'.*?_task-(?P<task>.+)_acq-(?P<acquisition>.+)_run-(?P<run>.+)_(?P<modality>cbv|bold)_tstat\.nii.gz',
		)
	df_ = df_roi_data(df_,
		mask_path=masks_dr[key],
		column_string='DR t',
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

# Create processing and template-independent unique identifiers
df['uID'] = df['subject']+'_'+df['session']+'_'+df['modality']

# Ready Strings for Printing
df['modality'] = df['modality'].str.upper()
df.columns = map(str.title, df.columns)
df = df.rename(
	columns={
		'Mean Dr T':'Mean DR t',
		'Median Dr T':'Median DR t',
		'Modality':'Contrast',
		})

df.to_csv('../data/functional_t.csv')
