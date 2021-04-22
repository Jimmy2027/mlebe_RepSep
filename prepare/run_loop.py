"""
This python-script runs the "run.sh" script with a number of models, selected from the results.csv.
Once one iteration of "run.sh" is finished, it deletes the registered images and only keeps the data that is needed to
create the article.
The article is then compiled and stored together with its data in the results folder.
"""

import os
from pathlib import Path

import norby
import pandas as pd
from mlebe.training.configs.utils import json_to_dict, write_to_jsonfile

from utils.general import verify_config_paths

nbr_tries = 5

# load model results table
model_results_table_path = os.path.expanduser('~/src/MLEBE_/mlebe/training/results.csv')
model_results_table = pd.read_csv(model_results_table_path)
model_results_table_anat = model_results_table.loc[model_results_table[
                                                       'data_type'] == 'anat'].sort_values('Overall_Dice',
                                                                                           ascending=False)[:nbr_tries]
model_results_table_func = model_results_table.loc[model_results_table[
                                                       'data_type'] == 'func'].sort_values('Overall_Dice',
                                                                                           ascending=False)[:nbr_tries]

config_dict_path = 'configs/noBiascorr_noCrop.json'
scratch_dir = Path('~/.scratch/mlebe').expanduser()

for index in range(nbr_tries):
    norby.send_msg(f'Starting workflow preparation nbr {index}.', add_loc_name=True)
    # load workflow results table
    workflow_results = pd.read_csv('classifier/reg_results.csv')
    # load config for the workflow
    config_dict = json_to_dict(config_dict_path)

    anat_model = model_results_table_anat.iloc[index]['config_path']
    func_model = model_results_table_func.iloc[index]['config_path']

    try:
        verify_config_paths(anat_model, func_model)
    except Exception as e:
        norby.send_msg(str(e))
        continue
    anat_model_uid = model_results_table_anat.iloc[index]['uid']
    func_model_uid = model_results_table_func.iloc[index]['uid']

    # check if this combination of anat_model and func_model has not been tried before:
    if not ((workflow_results['anat_model_uid'] == anat_model) & (
            workflow_results['func_model_uid'] == func_model)).any():
        # update config with new models
        write_to_jsonfile(config_dict_path, [('masking_config.masking_config_anat.model_config_path', anat_model),
                                             ('masking_config.masking_config_func.model_config_path', func_model)])
        print('starting workflow.')
        norby.send_msg(f'Starting workflow run nbr {index}.', add_loc_name=True)
        # run workflow
        assert os.system('./run.sh')
        assert scratch_dir.exists()
        crashdump_path = scratch_dir / 'preprocessing/crashdump'
        if crashdump_path.exists():
            norby.send_msg(f'Workflow did not execute cleanly, crashdump folder was created.')
            assert False
        norby.send_msg(f'Workflow run nbr {index} finished successfully. Starting to compile the article.',
                       add_loc_name=True)
        os.chdir('..')
        os.system('conda deactivate')
        # create article
        os.system('./cleanup.sh')
        os.system('./compile.sh mlebe article_ieeetm')

        article_path = scratch_dir / 'article_ieeetm.pdf'
        assert article_path.exists(), f'article was not created {article_path} does not exist.'
        norby.send_msg(f'Article was generated successfully.', add_loc_name=True)
        # move data to results folder
        out_folder = Path('results') / str(index)
        if not out_folder.exists():
            out_folder.mkdir(parents=True)
        for path in [scratch_dir / "data", article_path, scratch_dir / "config.json", scratch_dir / "config.json",
                     scratch_dir / 'manual_overview', scratch_dir / 'masking_vis']:
            os.system(f'mv {path} {out_folder}')
            assert (out_folder / path.name).exists()

        # remove scratch dir
        # os.system('rm -r {}'.format(os.path.expanduser('~/.scratch/mlebe')))
        norby.send_msg(
            f'Run nbr {index} finished successfully. The article can be found under {Path(os.getcwd()) / "results/{index}"}.',
            add_loc_name=True)
        sADFG
        os.chdir('prepare')
