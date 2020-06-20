"""
Pretrained models can be downloaded at: https://zenodo.org/record/3759361#.Xp70KlMzZQJ
"""
import uuid
import json
import os
import pandas as pd
import datetime

dir = '/home/hendrik/src/MLEBE/mlebe/threed/training/checkpoints/2020-06-15_anat_dice_loss_normalize_medic_blacklist_True1/'
anat_model_path = '/home/hendrik/src/MLEBE/mlebe/threed/training/checkpoints/2020-06-15_anat_dice_loss_normalize_medic_blacklist_True1/trained_mlebe_config_anat.json'
func_model_path = '/home/hendrik/src/MLEBE/mlebe/threed/training/checkpoints/2020-06-15_func_dice_loss_normalize_medic_blacklist False1/trained_mlebe_config_func.json'
scratch_dir = '~/.scratch/mlebe'
data_path = '/mnt/data/hendrik/mlebe_data/'
parameters = {  # parameters to be stored in the results dataframe
    'with_FLASH_train': True,
    'data_path': data_path,
    'date': str(datetime.date.today()),
    '3D_prediction': True,
    'blacklist': False,
}

if __name__ == '__main__':
    data = {'uid': uuid.uuid4().hex}
    assert not os.path.exists(
        os.path.expanduser(scratch_dir) + '/uid.json'), 'can not create uid, uid file already exists'

    with open(os.path.expanduser(scratch_dir) + '/uid.json', 'w') as json_file:
        json.dump(data, json_file)
    parameters['uid'] = data['uid']
    df = pd.DataFrame(parameters, index=[0])
    reg_results = pd.read_csv('classifier/reg_results.csv')
    reg_results = pd.concat([reg_results, df]).groupby('uid', as_index=False).first()
    reg_results.to_csv('classifier/reg_results.csv', index=False)

with open(os.path.expanduser(scratch_dir) + '/uid.json') as json_file:
    data = json.load(json_file)
uid = data['uid']

anat_model_training_config = anat_model_path.split('/')
anat_model_training_config[-1] = 'experiment_config.csv'
anat_model_training_config = '/'.join(anat_model_training_config)

func_model_training_config = func_model_path.split('/')
func_model_training_config[-1] = 'experiment_config.csv'
func_model_training_config = '/'.join(func_model_training_config)
