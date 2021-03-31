import os
from mlebe.training.configs.utils import json_to_dict, write_to_jsonfile


def verify_config_paths(anat_config, func_config):
    assert os.path.exists(anat_config), 'model_config_path ' + anat_config + ' does not exist'
    assert os.path.exists(func_config), 'model_config_path ' + func_config + ' does not exist'

    for model_config in [anat_config, func_config]:
        model_config_dict = json_to_dict(model_config)
        # attempt to fix path (wrapper for old paths)
        if not os.path.exists(model_config_dict['model']['path_pre_trained_model']):
            new_path = model_config_dict['model']['path_pre_trained_model'].replace('three_D/', '')
            if os.path.exists(new_path):
                write_to_jsonfile(model_config, [('model.path_pre_trained_model', new_path)])
        model_config_dict = json_to_dict(model_config)

        assert os.path.exists(
            model_config_dict['model']['path_pre_trained_model']), 'model path ' + \
                                                                   model_config_dict['model'][
                                                                       'path_pre_trained_model'] + ' does not exist'
