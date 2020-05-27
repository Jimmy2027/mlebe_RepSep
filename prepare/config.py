"""
Pretrained models can be downloaded with: https://zenodo.org/record/3759361#.Xp70KlMzZQJ
"""
import uuid
import json
import os
import pandas as pd

dir = '/mnt/data/hendrik/results/anat_br_augment/dice_600_2020-03-06/'
anat_model_path = '/mnt/data/hendrik/results/anat_br_augment/dice_600_2020-03-06/1_Step/model_ep282.h5'
func_model_path = '/mnt/data/hendrik/results/func_br_augment/dice_600_2020-03-07/1_Step/model_ep104.h5'
scratch_dir = '~/.scratch/mlebe'
data_path = '/mnt/data/hendrik/mlebe_trainingdata-1.0/'
parameters = {
    'with_FLASH': True,
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
