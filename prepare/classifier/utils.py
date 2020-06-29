import json

def set_cuda_var(config_path, use_cuda):
    with open(config_path) as file:
        config = json.load(file)
    config['model']['use_cuda'] = use_cuda
    with open(config_path, 'w') as outfile:
        json.dump(config, outfile, indent=4)



