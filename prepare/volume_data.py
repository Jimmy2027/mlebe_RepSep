from itertools import product
from os import path
from samri.report.snr import df_threshold_volume, iter_threshold_volume
import nibabel as nib
import numpy as np
import pandas as pd
from bids.grabbids import BIDSLayout
from bids.grabbids import BIDSValidator
from utils.bootstrapping import bootstrap, bootstrap_analysis
from make_config import CONFIG_PATH as config_path, SCRATCH_DIR as scratch_dir
from mlebe.training.utils.utils import json_file_to_pyobj
import os

workflow_config = json_file_to_pyobj(config_path)


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
base_df = base_df.loc[base_df['modality'].isin(['bold', 'cbv'])]
base_df['uID'] = base_df['subject'] + '_' + base_df['session'] + '_' + base_df['modality']

generic_df = pd.DataFrame()
masked_df = pd.DataFrame()
preprocessing_folders = ['preprocessing']
if workflow_config.workflow_config.with_FLASH:
    preprocessing_folders.append('preprocessing_dargcc')

for preprocessing_folder in preprocessing_folders:
    generic_df_ = bids_autograb('{}/{}/generic_collapsed'.format(scratch_dir, preprocessing_folder))
    generic_df_ = generic_df_.loc[~generic_df_['path'].str.endswith('.json')]
    generic_df_ = generic_df_.loc[generic_df_['modality'].isin(['bold', 'cbv'])]
    generic_df_['uID'] = generic_df_['subject'] + '_' + generic_df_['session'] + '_' + generic_df_['modality']
    generic_df = generic_df.append(generic_df_, ignore_index=True)

    masked_df_ = bids_autograb('{}/{}/masked_collapsed'.format(scratch_dir, preprocessing_folder))
    masked_df_ = masked_df_.loc[~masked_df_['path'].str.endswith('.json')]
    masked_df_ = masked_df_.loc[masked_df_['modality'].isin(['bold', 'cbv'])]
    masked_df_['uID'] = masked_df_['subject'] + '_' + masked_df_['session'] + '_' + masked_df_['modality']
    masked_df = masked_df.append(masked_df_, ignore_index=True)

uids = base_df['uID'].unique()
generic_df = generic_df.loc[generic_df['uID'].isin(uids)]
masked_df = masked_df.loc[masked_df['uID'].isin(uids)]

base_df['Processing'] = 'Unprocessed'
generic_df['Processing'] = 'Generic'
masked_df['Processing'] = 'Masked'

base_df['Threshold'] = ''
generic_df['Threshold'] = ''
masked_df['Threshold'] = ''

for uid in uids:
    img = nib.load(base_df.loc[base_df['uID'] == uid, 'path'].item())
    data = img.get_data()
    threshold = np.percentile(data, 66)
    base_df.loc[base_df['uID'] == uid, 'Threshold'] = threshold
    generic_df.loc[generic_df['uID'] == uid, 'Threshold'] = threshold
    masked_df.loc[masked_df['uID'] == uid, 'Threshold'] = threshold

df = pd.DataFrame([])
df_ = df_threshold_volume(base_df,
                          threshold='Threshold',
                          )
df = df.append(df_)
df_ = df_threshold_volume(generic_df,
                          threshold='Threshold',
                          )
df = df.append(df_)
df_ = df_threshold_volume(masked_df,
                          threshold='Threshold',
                          )
df = df.append(df_)

# Ar a voxel size of 0.2mm isotropic we are only sensitive to about 0.008mm^3
df = df.round({'Volume': 3, 'Thresholded Volume': 3})

# Calculate Volume Conservation Factor
df['Volume Conservation Factor'] = -1
df['Abs(1 - Vcf)'] = -1
uids = df['uID'].unique()

processings = [i for i in df['Processing'].unique() if i != 'Unprocessed']
for uid, processing in list(product(uids, processings)):
    reference = df.loc[(df['uID'] == uid) & (df['Processing'] == 'Unprocessed'), 'Thresholded Volume'].item()
    volume = df.loc[(df['uID'] == uid) & (df['Processing'] == processing), 'Thresholded Volume'].item()
    df.loc[(df['uID'] == uid) & (df['Processing'] == processing), 'Volume Conservation Factor'] = volume / reference
    df.loc[(df['uID'] == uid) & (df['Processing'] == processing), 'Abs(1 - Vcf)'] = np.abs(1 - volume / reference)

# Ready Strings for Printing
df['modality'] = df['modality'].str.upper()
df = df.rename(columns={'modality': 'Contrast', })
df.columns = map(str.title, df.columns)
if workflow_config.workflow_config.with_FLASH:
    df.loc[df['Uid'].str.contains('VZ'), 'Contrast'] = 'T1w+' + df.loc[df['Uid'].str.contains('VZ'), 'Contrast']
    df.loc[~df['Uid'].str.contains('VZ'), 'Contrast'] = 'T2w+' + df.loc[~df['Uid'].str.contains('VZ'), 'Contrast']

df.to_csv(path.join(scratch_dir, 'data', 'volume.csv'))

"""
Bootstrapping
"""
bootstrap(df, 'Volume Conservation Factor', scratch_dir=scratch_dir, nbr_samples=len(df))
bootstrap_analysis('volume', dependent_variable='VCF_RMSE', expression='Processing*Contrast', scratch_dir=scratch_dir,
                   nbr_samples=len(df))
"""
Writing results
"""
anat_model_training_config = json_file_to_pyobj(workflow_config.masking_config.masking_config_anat.model_config_path)
func_model_training_config = json_file_to_pyobj(workflow_config.masking_config.masking_config_func.model_config_path)

if not os.path.exists('classifier/reg_results.csv'):
    reg_results_ = pd.DataFrame([[]])
else:
    reg_results_ = pd.read_csv('classifier/reg_results.csv')
reg_results = pd.DataFrame([[]])
reg_results['uid'] = workflow_config.workflow_config.uid
reg_results['anat_model_uid'] = anat_model_training_config.model.uid
reg_results['func_model_uid'] = func_model_training_config.model.uid
reg_results['anat_model_path'] = workflow_config.masking_config.masking_config_anat.model_config_path
reg_results['func_model_path'] = workflow_config.masking_config.masking_config_func.model_config_path
reg_results['func_model_dice'] = workflow_config.masking_config.masking_config_func.dice_score
reg_results['anat_model_dice'] = workflow_config.masking_config.masking_config_anat.dice_score
reg_results['masked_mean_Vcf_RMSE'] = df.loc[df['Processing'] == 'Masked', 'Abs(1 - Vcf)'].mean()
reg_results['generic_mean_Vcf_RMSE'] = df.loc[df['Processing'] == 'Generic', 'Abs(1 - Vcf)'].mean()
reg_results['max_RMSE_generic'] = -1
reg_results['max_RMSE_generic'] = reg_results['max_RMSE_generic'].astype('object')
reg_results.at[0, 'max_RMSE_generic'] = [df.loc[df['Processing'] == 'Generic'].groupby('Uid')['Abs(1 - Vcf)'].max().idxmax(),
                                         df.loc[df['Processing'] == 'Generic'].groupby('Uid')['Abs(1 - Vcf)'].max().max()]
reg_results['max_RMSE_masked'] = -1
reg_results['max_RMSE_masked'] = reg_results['max_RMSE_masked'].astype('object')
reg_results.at[0, 'max_RMSE_masked'] = [df.loc[df['Processing'] == 'Masked'].groupby('Uid')['Abs(1 - Vcf)'].max().idxmax(),
                                        df.loc[df['Processing'] == 'Masked'].groupby('Uid')['Abs(1 - Vcf)'].max().max()]

if workflow_config.workflow_config.uid in reg_results_['uid'].to_list():
    reg_results_ = pd.concat([reg_results, reg_results_]).groupby('uid', as_index=False).first()
else:
    reg_results_ = reg_results_.append(reg_results)


reg_results_.to_csv('classifier/reg_results.csv', index=False)
