from samri.pipelines import manipulations
from make_config import config_path, scratch_dir
from mlebe.training.configs.utils import json_to_dict

config = json_to_dict(config_path)
if config['workflow_config']['with_FLASH']:
    bids_bases = ['{}/bids'.format(scratch_dir), '{}/dargcc_bids'.format(scratch_dir)]
else:
    bids_bases = ['{}/bids'.format(scratch_dir)]
for bids_base in bids_bases:
    # Create 3D collapsed dataset to speed up repeated evaluations
    # Uncomment n_jobs_percentage parameter for machines with limited memory,
    # or comment them out for machines with plenty of memory.
    manipulations.collapse_nifti(bids_base,
                                 '{}/bids_collapsed'.format(scratch_dir),
                                 n_jobs_percentage=0.66,
                                 )
if config['workflow_config']['with_FLASH']:
    manipulations.collapse_nifti('{}/preprocessing_dargcc/masked'.format(scratch_dir),
                                 '{}/preprocessing_dargcc/masked_collapsed'.format(scratch_dir),
                                 n_jobs_percentage=0.33,
                                 )

    manipulations.collapse_nifti('{}/preprocessing_dargcc/generic'.format(scratch_dir),
                                 '{}/preprocessing_dargcc/generic_collapsed'.format(scratch_dir),
                                 n_jobs_percentage=0.33,
                                 )

manipulations.collapse_nifti('{}/preprocessing/masked'.format(scratch_dir),
                             '{}/preprocessing/masked_collapsed'.format(scratch_dir),
                             n_jobs_percentage=0.33,
                             )

manipulations.collapse_nifti('{}/preprocessing/generic'.format(scratch_dir),
                             '{}/preprocessing/generic_collapsed'.format(scratch_dir),
                             n_jobs_percentage=0.33,
                             )
