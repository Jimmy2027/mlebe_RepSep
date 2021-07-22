from os import path

from mlebe.training.configs.utils import json_to_dict
from norby.utils import maybe_norby
from samri.pipelines import glm

from make_config import CONFIG_PATH as config_path

config = json_to_dict(config_path)
scratch_dir = '~/.scratch/mlebe'

preprocess_base = '{}/preprocessing/'.format(scratch_dir)

masks = {
    'generic': '/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
    'masked': '/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
}

with maybe_norby(config['workflow_config']['norby'], 'starting l1', 'l1 finished', whichbot='mlebe'):
    for key in masks:
        glm.l1(path.join(preprocess_base, key),
               bf_path='../data/chr_beta1.txt',
               workflow_name=key,
               habituation="confound",
               mask=masks[key],
               keep_work=False,
               n_jobs_percentage=.33,
               match={'suffix': ['cbv']},
               exclude={'task': ['rest']},
               invert=True,
               out_base='{}/l1'.format(scratch_dir)
               )
        glm.l1(path.join(preprocess_base, key),
               bf_path='../data/chr_beta1.txt',
               workflow_name=key,
               habituation="confound",
               mask=masks[key],
               keep_work=False,
               n_jobs_percentage=.33,
               match={'suffix': ['bold']},
               exclude={'task': ['rest']},
               invert=False,
               out_base='{}/l1'.format(scratch_dir)
               )
