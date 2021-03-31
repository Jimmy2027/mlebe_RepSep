"""
Pretrained models can be downloaded at: https://zenodo.org/record/3759361#.Xp70KlMzZQJ
"""
import datetime
import os
import uuid
from pathlib import Path
from shutil import copyfile

import pandas as pd
from mlebe.training.configs.utils import json_to_dict, write_to_jsonfile
from mlebe.training.utils.utils import mkdir

# choose your workflow configuration
JSON_CONFIG_PATH = Path(__file__).parent / "configs/noBiascorr_noCrop.json"
SCRATCH_DIR = Path('~/.scratch/mlebe').expanduser()
CONFIG_PATH = os.path.expanduser(os.path.join(SCRATCH_DIR, 'config.json'))


def prepare_config(json_config_path: Path, scratch_dir: Path):
    mkdir(os.path.expanduser(scratch_dir))
    config = json_to_dict(json_config_path)
    # copy the json configuration file to the scratch directory
    new_config_path = scratch_dir / 'config.json'
    verify_config_path(new_config_path)
    copyfile(json_config_path, new_config_path)
    # prepare the workflow config file
    workflow_uid = uuid.uuid4().hex

    # write workflow uid and model dice scores to new workflow config
    write_to_jsonfile(new_config_path, [('workflow_config.uid', workflow_uid)])
    return config, workflow_uid


def prepare_experiment_result_dataframe(config: dict, workflow_uid: str):
    # prepare the experiment result dataframe
    parameters = {'with_FLASH': config['workflow_config']['with_FLASH'], 'date': str(datetime.date.today()),
                  'masking_with_bias_corr_anat-func': '{}/ {}'.format(
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
    CONFIG, WORKFLOW_UID = prepare_config(JSON_CONFIG_PATH, SCRATCH_DIR)
    prepare_experiment_result_dataframe(config=CONFIG, workflow_uid=WORKFLOW_UID)
