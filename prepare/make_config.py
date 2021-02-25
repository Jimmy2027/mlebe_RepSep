"""
Pretrained models can be downloaded at: https://zenodo.org/record/3759361#.Xp70KlMzZQJ
"""
import datetime
import os
import uuid
from shutil import copyfile

import pandas as pd
from mlebe.training.configs.utils import json_to_dict, write_to_jsonfile, get_dice_score_of_model
from mlebe.training.utils.utils import mkdir

from classifier.utils import init_model_configs
from pathlib import Path

# choose your workflow configuration
JSON_CONFIG_PATH = Path(__file__).parent / "configs/noBiascorr_noCrop.json"
EXPERIMENT_RESULTS_DF_PATH = os.path.expanduser('~/src/MLEBE/mlebe/training/results.csv')
SCRATCH_DIR = '~/.scratch/mlebe'
CONFIG_PATH = os.path.expanduser(os.path.join(SCRATCH_DIR, 'config.json'))


def prepare_config(json_config_path: str, scratch_dir: str, experiment_results_df_path: str):
    mkdir(os.path.expanduser(scratch_dir))
    config = json_to_dict(json_config_path)
    # overwrite parameters of the model configs such as use_cuda, etc... for the workflow
    init_model_configs(config)
    # copy the json configuration file to the scratch directory
    new_config_path = os.path.expanduser(os.path.join(scratch_dir, 'config.json'))
    verify_config_path(new_config_path)
    copyfile(json_config_path, new_config_path)
    # prepare the workflow config file
    workflow_uid = uuid.uuid4().hex
    anat_model_config_path = config['masking_config']['masking_config_anat'][
                                 'model_folder_path'] + '/trained_mlebe_config_anat.json'
    func_model_config_path = config['masking_config']['masking_config_func'][
                                 'model_folder_path'] + '/trained_mlebe_config_func.json'
    # write workflow uid and model dice scores to new workflow config
    write_to_jsonfile(new_config_path, [('workflow_config.uid', workflow_uid),
                                        ('masking_config.masking_config_anat.dice_score',
                                         get_dice_score_of_model(anat_model_config_path, experiment_results_df_path)),
                                        ('masking_config.masking_config_func.dice_score',
                                         get_dice_score_of_model(func_model_config_path, experiment_results_df_path))])
    return config, workflow_uid


def prepare_experiment_result_dataframe(config: dict, workflow_uid: str):
    # prepare the experiment result dataframe
    parameters = {'with_FLASH': config['workflow_config']['with_FLASH'], 'date': str(datetime.date.today()),
                  '3D_prediction': True, 'masking_with_bias_corr_anat-func': '{}/ {}'.format(
            config['masking_config']['masking_config_anat']['bias_correct_bool'],
            config['masking_config']['masking_config_func']['bias_correct_bool']),
                  'masking_with_cropping': '{}/ {}'.format(
                      config['masking_config']['masking_config_anat']['with_bids_cropping'],
                      config['masking_config']['masking_config_func']['with_bids_cropping']), 'uid': workflow_uid}
    df = pd.DataFrame(parameters, index=[0])
    reg_results = pd.read_csv('classifier/reg_results.csv')
    reg_results = pd.concat([reg_results, df]).groupby('uid', as_index=False).first()
    reg_results.to_csv('classifier/reg_results.csv', index=False)


def verify_config_path(config_path):
    assert not os.path.exists(
        config_path), 'can not initiate new config, a config file already exists at {}. ' \
                      'Erase the old one or rename its folder to not overwrite old results'.format(config_path)


if __name__ == '__main__':
    CONFIG, WORKFLOW_UID = prepare_config(JSON_CONFIG_PATH, SCRATCH_DIR,
                                          experiment_results_df_path=EXPERIMENT_RESULTS_DF_PATH)
    prepare_experiment_result_dataframe(config=CONFIG, workflow_uid=WORKFLOW_UID)
