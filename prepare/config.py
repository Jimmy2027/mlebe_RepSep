"""
Pretrained models can be downloaded with: https://zenodo.org/record/3759361#.Xp70KlMzZQJ
"""
import uuid
import json
import os

dir = '/mnt/data/mlebe_data/results/anat_br_augment/dice_600_2020-03-06/'
anat_model_path = '/mnt/data/mlebe_data/results/anat_br_augment/dice_600_2020-03-06/1_Step/model_ep282.h5'
func_model_path = '/mnt/data/mlebe_data/results/func_br_augment/dice_600_2020-03-07/1_Step/model_ep104.h5'
scratch_dir = '~/.scratch/mlebe_final'

if __name__ == '__main__':
    data = {'uid': uuid.uuid4().hex}
    with open(os.path.expanduser(scratch_dir) + '/uid.json', 'w') as json_file:
        json.dump(data, json_file)

# training_config = dir + '1_Step/experiment_config.csv'
with open(os.path.expanduser(scratch_dir) + '/uid.json') as json_file:
    data = json.load(json_file)
uid = data['uid']

anat_model_training_config = anat_model_path.split('/')
anat_model_training_config[-1] = 'experiment_config.csv'
anat_model_training_config = '/'.join(anat_model_training_config)

func_model_training_config = func_model_path.split('/')
func_model_training_config[-1] = 'experiment_config.csv'
func_model_training_config = '/'.join(func_model_training_config)