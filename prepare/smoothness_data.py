import os
from os import path

import numpy as np
import pandas as pd
from bids.layout import BIDSLayout
from mlebe.training.utils.utils import json_file_to_pyobj

from make_config import CONFIG_PATH as config_path, SCRATCH_DIR as scratch_dir
from utils.bootstrapping import bootstrap, bootstrap_analysis

masks = {
    'generic': '/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
    'masked': '/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
}


def bids_autograb(bids_dir):
    bids_dir = path.abspath(path.expanduser(bids_dir))
    layout = BIDSLayout(bids_dir, validate=False)
    df = layout.to_df()

    # Unclear in current BIDS specification, we refer to BOLD/CBV as modalities and func/anat as types
    df = df.rename(columns={'datatype': 'type', 'suffix': 'modality'})
    return df


def avg_smoothness(inp_file):
    from nipype.interfaces import afni
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
    if ('bold' in inp_entry):
        return 'bold'
    else:
        return 'cbv'


workflow_config = json_file_to_pyobj(config_path)
preprocessing_folders = ['preprocessing']
if workflow_config.workflow_config.with_FLASH:
    preprocessing_folders.append('preprocessing_dargcc')

df_bids = bids_autograb(scratch_dir / 'bids_collapsed/')
df_bids['Processing'] = 'Unprocessed'
df_generic = pd.DataFrame()
df_masked = pd.DataFrame()
for preprocessing_folder in preprocessing_folders:
    df_generic = df_generic.append(bids_autograb(scratch_dir / '{}/generic_collapsed/'.format(preprocessing_folder)))
    df_masked = df_masked.append(bids_autograb(scratch_dir / '{}/masked_collapsed/'.format(preprocessing_folder)))
df_generic['Processing'] = 'Generic'
df_masked['Processing'] = 'Masked'

df = pd.concat([df_generic, df_masked, df_bids])
df['Uid'] = df['subject'] + '_' + df['session'] + '_' + df['modality']
df = df[df['type'] == 'func']

# df = df.loc[np.logical_or(df.modality == 'cbv', df.modality == 'bold')]
# df['modality'] = df['modality'].str.upper()
# df['Contrast'] = df['modality']
df['Contrast'] = df['modality']
df['Contrast'] = df['Contrast'].str.upper()
if workflow_config.workflow_config.with_FLASH:
    df.loc[df['Uid'].str.contains('VZ'), 'Contrast'] = 'T1w+' + df.loc[df['Uid'].str.contains('VZ'), 'Contrast']
    df.loc[~df['Uid'].str.contains('VZ'), 'Contrast'] = 'T2w+' + df.loc[~df['Uid'].str.contains('VZ'), 'Contrast']
else:
    df.loc[~df['Uid'].str.contains('VZ'), 'Contrast'] = df.loc[~df['Uid'].str.contains('VZ'), 'Contrast']

df['Smoothness'] = df['path'].apply(avg_smoothness)

df['Smoothness Conservation Factor'] = ''
df.to_csv(path.join(scratch_dir, 'data', 'df.csv'))
uids = df['Uid'].unique()
for uid in uids:
    if not df.loc[(df['Uid'] == uid) & (df['Processing'] == 'Unprocessed'), 'Smoothness'].empty:
        original = df.loc[(df['Uid'] == uid) & (df['Processing'] == 'Unprocessed'), 'Smoothness'].item()
        df.loc[(df['Uid'] == uid), 'Smoothness Conservation Factor'] = df.loc[
                                                                           (df['Uid'] == uid), 'Smoothness'] / original

v_path = path.join(scratch_dir, 'data', 'volume.csv')

v = pd.read_csv(v_path)
df = df.reset_index()
df['Volume-Normalized SCF'] = 0
df['Abs(1 - Scf)'] = -1

for uid in df['Uid'].unique():
    for p in ['Generic', 'Masked']:
        if not df.loc[(df['Uid'] == uid) & (df['Processing'] == p), 'Smoothness Conservation Factor'].empty and not \
                v.loc[(v['Uid'] == uid) & (v['Processing'] == p), 'Volume Conservation Factor'].empty:
            scf = df.loc[(df['Uid'] == uid) & (df['Processing'] == p), 'Smoothness Conservation Factor'].item()
            vcf = v.loc[(v['Uid'] == uid) & (v['Processing'] == p), 'Volume Conservation Factor'].item()
            df.loc[(df['Uid'] == uid) & (df['Processing'] == p), 'Volume-Normalized SCF'] = scf / (vcf ** (1. / 3.))
            df.loc[(df['Uid'] == uid) & (df['Processing'] == p), 'Abs(1 - Scf)'] = np.abs(
                1 - (scf / (vcf ** (1. / 3.))))

df.to_csv(path.join(scratch_dir, 'data', 'smoothness.csv'))

files = os.listdir('./')
for _file in files:
    if _file.endswith(('.out', '.1D')):
        os.remove(path.abspath(path.expanduser(_file)))

"""
Bootstrapping
"""
bootstrap(df, 'Smoothness Conservation Factor', scratch_dir, nbr_samples=len(df))
bootstrap_analysis('smoothness', dependent_variable='SCF_RMSE', expression='Processing*Contrast',
                   scratch_dir=scratch_dir, nbr_samples=len(df))

"""
Writing results
"""

reg_results = pd.DataFrame([[]])
reg_results['uid'] = workflow_config.workflow_config.uid
reg_results['masked_mean_Scf_RMSE'] = df.loc[df['Processing'] == 'Masked', 'Abs(1 - Scf)'].mean()
reg_results['generic_mean_Scf_RMSE'] = df.loc[df['Processing'] == 'Generic', 'Abs(1 - Scf)'].mean()
reg_results['max_Scf_RMSE_generic'] = -1
reg_results['max_Scf_RMSE_generic'] = reg_results['max_Scf_RMSE_generic'].astype('object')
reg_results.at[0, 'max_Scf_RMSE_generic'] = (
    df.loc[df['Processing'] == 'Generic'].groupby('Uid')['Abs(1 - Scf)'].max().idxmax(),
    df.loc[df['Processing'] == 'Generic'].groupby('Uid')['Abs(1 - Scf)'].max().max())
reg_results['max_Scf_RMSE_masked'] = -1
reg_results['max_Scf_RMSE_masked'] = reg_results['max_Scf_RMSE_masked'].astype('object')
reg_results.at[0, 'max_Scf_RMSE_masked'] = (
    df.loc[df['Processing'] == 'Masked'].groupby('Uid')['Abs(1 - Scf)'].max().idxmax(),
    df.loc[df['Processing'] == 'Masked'].groupby('Uid')['Abs(1 - Scf)'].max().max())

reg_results_ = pd.read_csv('classifier/reg_results.csv')
reg_results_ = pd.concat([reg_results, reg_results_]).groupby('uid', as_index=False).first()
reg_results_.to_csv('classifier/reg_results.csv', index=False)
