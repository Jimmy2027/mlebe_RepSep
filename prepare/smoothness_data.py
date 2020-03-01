from itertools import product
from os import path
import os
from samri.report.snr import df_threshold_volume ,iter_threshold_volume
import nibabel as nib
import numpy as np
import pandas as pd
from bids.grabbids import BIDSLayout
from bids.grabbids import BIDSValidator
import nipype.interfaces.io as nio

masks = {
	'generic':'/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
	'generic_masked':'/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
	}

def bids_autograb(bids_dir):
	bids_dir = path.abspath(path.expanduser(bids_dir))
	validate = BIDSValidator()
	layout = BIDSLayout(bids_dir)
	df = layout.as_data_frame()

	# Unclear in current BIDS specification, we refer to BOLD/CBV as modalities and func/anat as types
	df = df.rename(columns={'modality': 'type', 'type': 'modality'})
	return df

def avg_smoothness(inp_file):
	from nipype.interfaces import afni
	import numpy as np
	fwhm = afni.FWHMx()

	# use automask so it's consistent for raw as well as preprocessed data
	fwhm.inputs.automask = True

	# detrending option
	fwhm.inputs.detrend = True

	fwhm.inputs.in_file = inp_file
	fwhm.inputs.acf = True
	fwhm_run = fwhm.run()
	# It appears the new/correct FWHM is now located under the last position of the ACF estimates.
	# https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dFWHMx.html
	res = fwhm_run.outputs.acf_param[3]
	return res

def acqname(inp_entry):
	if('bold' in  inp_entry):
		return 'bold'
	else:
		return 'cbv'

scratch_dir = '~/.scratch/mlebe'

df_bids = bids_autograb(scratch_dir + '/bids_collapsed/')
df_bids['Processing'] = 'Unprocessed'

df_generic = bids_autograb(scratch_dir + '/preprocessing/generic_collapsed/')
df_generic['Processing'] = 'Generic'

df_generic_masked = bids_autograb(scratch_dir + '/preprocessing/generic_masked_collapsed/')
df_generic_masked['Processing'] = 'Generic Masked'

df = pd.concat([df_generic, df_generic_masked, df_bids])
df['Uid'] = df['subject']+'_'+df['session']+'_'+df['modality']
df = df[df['type']=='func']

df = df.loc[np.logical_or(df.modality == 'cbv', df.modality == 'bold')]
df['modality'] = df['modality'].str.upper()
df['Contrast'] = df['modality']

df['Smoothness'] = df['path'].apply(avg_smoothness)
# df.loc[df['Processing']=='Legacy', 'Smoothness'] = df.loc[df['Processing']=='Legacy', 'Smoothness']/10

df['Smoothness Conservation Factor'] = ''
uids = df['Uid'].unique()
for uid in uids:
	original = df.loc[(df['Uid']==uid) & (df['Processing']=='Unprocessed'), 'Smoothness'].item()
	df.loc[(df['Uid']==uid), 'Smoothness Conservation Factor'] = df.loc[(df['Uid']==uid), 'Smoothness'] / original

v_path= path.join(scratch_dir, 'data', 'volume.csv')

v = pd.read_csv(v_path)
df = df.reset_index()
df['Volume-Normalized SCF'] = 0
for uid in df['Uid'].unique():
	# for p, t in product(['Generic', 'Legacy'],['Generic','Legacy']):
	for p, t in product(['Generic', 'Generic Masked'], ['Generic', 'Generic Masked']):
		# scf = df.loc[(df['Uid']==uid)&(df['Processing']==p)&(df['Template']==t),'Smoothness Conservation Factor'].item()
		# vcf = v.loc[(v['Uid']==uid)&(v['Processing']==p)&(v['Template']==t),'Volume Conservation Factor'].item()
		# df.loc[(df['Uid']==uid)&(df['Processing']==p)&(df['Template']==t),'Volume-Normalized SCF'] = scf/(vcf**(1./3.))
		scf = df.loc[(df['Uid']==uid)&(df['Processing']==p),'Smoothness Conservation Factor'].item()
		vcf = v.loc[(v['Uid']==uid)&(v['Processing']==p),'Volume Conservation Factor'].item()
		df.loc[(df['Uid']==uid)&(df['Processing']==p),'Volume-Normalized SCF'] = scf/(vcf**(1./3.))

df.to_csv(path.join(scratch_dir, 'data', 'smoothness.csv'))

files = os.listdir('./')
for _file in files:
	if _file.endswith(('.out','.1D')):
		os.remove(path.abspath(path.expanduser(_file)))
