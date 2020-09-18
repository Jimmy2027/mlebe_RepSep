"""
This python-script runs the "run.sh" script with a number of models, selected from the results.csv.
Once one iteration of "run.sh" is finished, it deletes the registered images and only keeps the data that is needed to
create the article.
The article is then compiled and stored together with its data in the results folder.
"""
import os
import pandas as pd
from mlebe.training.configs.utils import json_to_dict, write_to_jsonfile
from mlebe.training.utils.utils import mkdir
from utils.general import verify_config_paths

nbr_tries = 5

# load model results table
model_results_table_path = os.path.expanduser('~/src/MLEBE/mlebe/training/results.csv')
model_results_table = pd.read_csv(model_results_table_path)
model_results_table_anat = model_results_table.loc[model_results_table[
                                                       'data_type'] == 'anat'].sort_values('Overall_Dice',
                                                                                           ascending=False)[:nbr_tries]
model_results_table_func = model_results_table.loc[model_results_table[
                                                       'data_type'] == 'func'].sort_values('Overall_Dice',
                                                                                           ascending=False)[:nbr_tries]

config_dict_path = 'configs/noBiascorr_noCrop.json'

for index in range(nbr_tries):
    # load workflow results table
    workflow_results = pd.read_csv('classifier/reg_results.csv')
    # load config for the workflow
    config_dict = json_to_dict(config_dict_path)

    anat_model = model_results_table_anat.iloc[index]['config_path']
    func_model = model_results_table_func.iloc[index]['config_path']

    verify_config_paths(anat_model, func_model)

    anat_model_uid = model_results_table_anat.iloc[index]['uid']
    func_model_uid = model_results_table_func.iloc[index]['uid']

    # check if this combination of anat_model and func_model has not been tried before:
    if not ((workflow_results['anat_model_uid'] == anat_model) & (
            workflow_results['func_model_uid'] == func_model)).any():
        # update config with new models
        write_to_jsonfile(config_dict_path, [('masking_config.masking_config_anat.model_config_path', anat_model),
                                             ('masking_config.masking_config_func.model_config_path', func_model)])

        # run workflow
        os.system('./run.sh')
        # create article
        os.system('../cleanup.sh')
        os.system('../compile.sh mlebe')

        # move data to results folder
        dir_name = index
        mkdir('results/{}'.format(dir_name))
        os.system('mv {} results/{}'.format(os.path.expanduser('~/.scratch/mlebe/data'), dir_name))
        os.system('mv {} results/{}'.format(os.path.expanduser('~/.scratch/mlebe/article.pdf'), dir_name))
        os.system('mv {} results/{}'.format(os.path.expanduser('~/.scratch/mlebe/config.json'), dir_name))

        # remove scratch dir
        os.system('rm -r {}'.format(os.path.expanduser('~/.scratch/mlebe')))
