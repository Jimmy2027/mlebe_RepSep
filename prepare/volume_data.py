from itertools import product
from os import path
from samri.report.snr import df_threshold_volume, iter_threshold_volume
import nibabel as nib
import numpy as np
import pandas as pd
from bids.grabbids import BIDSLayout
from bids.grabbids import BIDSValidator
from utils.bootstrapping import bootstrap, bootstrap_analysis
import config
import os

scratch_dir = config.scratch_dir


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

generic_df = bids_autograb('{}/preprocessing/generic_collapsed'.format(scratch_dir))
generic_df = generic_df.loc[~generic_df['path'].str.endswith('.json')]
generic_df = generic_df.loc[generic_df['modality'].isin(['bold', 'cbv'])]
generic_df['uID'] = generic_df['subject'] + '_' + generic_df['session'] + '_' + generic_df['modality']

masked_df = bids_autograb('{}/preprocessing/masked_collapsed'.format(scratch_dir))
masked_df = masked_df.loc[~masked_df['path'].str.endswith('.json')]
masked_df = masked_df.loc[masked_df['modality'].isin(['bold', 'cbv'])]
masked_df['uID'] = masked_df['subject'] + '_' + masked_df['session'] + '_' + masked_df['modality']

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
df['1 - Vcf'] = -1
uids = df['uID'].unique()

processings = [i for i in df['Processing'].unique() if i != 'Unprocessed']
for uid, processing in list(product(uids, processings)):
    reference = df.loc[(df['uID'] == uid) & (df['Processing'] == 'Unprocessed'), 'Thresholded Volume'].item()
    try:
        volume = df.loc[(df['uID'] == uid) & (df['Processing'] == processing), 'Thresholded Volume'].item()
    except:
        volume = 1
        print(uid, processing)
    df.loc[(df['uID'] == uid) & (df['Processing'] == processing), 'Volume Conservation Factor'] = volume / reference
    df.loc[(df['uID'] == uid) & (df['Processing'] == processing), '1 - Vcf'] = np.abs(1 - volume / reference)

# Ready Strings for Printing
df['modality'] = df['modality'].str.upper()
df = df.rename(columns={'modality': 'Contrast', })
df.columns = map(str.title, df.columns)
df.to_csv(path.join(scratch_dir, 'data', 'volume.csv'))

"""
Bootstrapping
"""
bootstrap(df, 'Volume Conservation Factor', scratch_dir=scratch_dir)
bootstrap_analysis('volume', dependent_variable='VCF_RMSE', expression='Processing*Contrast', scratch_dir=scratch_dir)
"""
Writing results
"""
anat_model_training_config = pd.read_csv(config.anat_model_training_config)
func_model_training_config = pd.read_csv(config.func_model_training_config)

if not os.path.exists('classifier/reg_results.csv'):
    reg_results_ = pd.DataFrame([[]])
else:
    reg_results_ = pd.read_csv('classifier/reg_results.csv')
reg_results = pd.DataFrame([[]])
reg_results['uid'] = config.uid
reg_results['anat_model_uid'] = anat_model_training_config['uid'].item()
reg_results['func_model_uid'] = func_model_training_config['uid'].item()
reg_results['anat_model_path'] = config.anat_model_path
reg_results['func_model_path'] = config.func_model_path
reg_results['func_model_dice'] = func_model_training_config['dice_score'].item()
reg_results['anat_model_dice'] = anat_model_training_config['dice_score'].item()
reg_results['masked_mean_Vcf_RMSE'] = df.loc[df['Processing'] == 'Masked', '1 - Vcf'].mean()
reg_results['generic_mean_Vcf_RMSE'] = df.loc[df['Processing'] == 'Generic', '1 - Vcf'].mean()
reg_results['max_RMSE_generic'] = -1
reg_results['max_RMSE_generic'] = reg_results['max_RMSE_generic'].astype('object')
reg_results.at[0,'max_RMSE_generic'] = [df.loc[df['Processing'] == 'Generic'].groupby('Uid')['1 - Vcf'].max().idxmax(),
                                         df.loc[df['Processing'] == 'Generic'].groupby('Uid')['1 - Vcf'].max().max()]
reg_results['max_RMSE_masked'] = -1
reg_results['max_RMSE_masked'] = reg_results['max_RMSE_masked'].astype('object')
reg_results.at[0,'max_RMSE_masked'] = [df.loc[df['Processing'] == 'Masked'].groupby('Uid')['1 - Vcf'].max().idxmax(),
                                        df.loc[df['Processing'] == 'Masked'].groupby('Uid')['1 - Vcf'].max().max()]

reg_results_ = reg_results_.append(reg_results)
reg_results_.to_csv('classifier/reg_results.csv', index=False)

