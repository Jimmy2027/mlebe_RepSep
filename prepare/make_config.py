"""
Pretrained models can be downloaded at: https://zenodo.org/record/3759361#.Xp70KlMzZQJ
"""
import datetime
import os
import uuid
from shutil import copyfile
import pandas as pd
from mlebe.training.three_D.configs.utils import json_to_dict, write_to_jsonfile, get_dice_score_of_model
from mlebe.training.three_D.utils.utils import mkdir
from classifier.utils import init_model_configs

scratch_dir = '~/.scratch/mlebe'
config_path = os.path.expanduser(os.path.join(scratch_dir, 'config.json'))

if __name__ == '__main__':
    mkdir(os.path.expanduser(scratch_dir))
    # choose your workflow configuration
    json_config_path = "configs/with_bias_corr.json"
    config = json_to_dict(json_config_path)
    # initialise model configs
    init_model_configs(config)
    # copy the json configuration file to the scratch directory
    new_config_path = os.path.expanduser(os.path.join(scratch_dir, 'config.json'))
    assert not os.path.exists(
        new_config_path), 'can not initiate new config, a config file already exists at {}. Erase the old one or rename its folder to not overwrite old results'.format(
        new_config_path)
    copyfile(json_config_path, new_config_path)
    # prepare the workflow config file
    workflow_uid = uuid.uuid4().hex
    write_to_jsonfile(new_config_path, [('workflow_config.uid', workflow_uid),
                                        ('masking_config.masking_config_anat.dice_score',
                                         get_dice_score_of_model(
                                             config['masking_config']['masking_config_anat']['model_config_path'])),
                                        ('masking_config.masking_config_func.dice_score', get_dice_score_of_model(
                                            config['masking_config']['masking_config_func']['model_config_path']))])

    # prepare the experiment result dataframe
    parameters = {  # parameters to be stored in the results dataframe
        'with_FLASH': config['workflow_config']['with_FLASH'],
        'date': str(datetime.date.today()),
        '3D_prediction': True,
    }
    parameters['uid'] = workflow_uid
    df = pd.DataFrame(parameters, index=[0])
    reg_results = pd.read_csv('classifier/reg_results.csv')
    reg_results = pd.concat([reg_results, df]).groupby('uid', as_index=False).first()
    reg_results.to_csv('classifier/reg_results.csv', index=False)
