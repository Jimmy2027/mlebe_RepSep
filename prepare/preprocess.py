from mlebe.training.configs.utils import json_to_dict
from norby import send_msg
from samri.pipelines.preprocess import generic

from make_config import CONFIG_PATH as config_path, SCRATCH_DIR as scratch_dir

config = json_to_dict(config_path)
if config['workflow_config']['norby']:
    send_msg(f'Starting preprocess.', add_loc_name=True)

subjects = config['workflow_config']['subjects']
bids_base = '{}/bids'.format(scratch_dir)
template_path = '/usr/share/mouse-brain-atlases/dsurqec_200micron.nii'
registration_mask = '/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii'
# Preprocess all of the data:
if config['workflow_config']['with_FLASH']:
    dargcc_bids_base = '{}/dargcc_bids'.format(scratch_dir)

    generic(dargcc_bids_base,
            template_path,
            registration_mask=registration_mask,
            functional_match={'acquisition': ['EPI'], },
            structural_match={'acquisition': ['FLASH'], },
            out_base='{}/preprocessing_dargcc'.format(scratch_dir),
            workflow_name='masked',
            keep_work=config['workflow_config']['keep_work'],
            masking_config_path=config_path,
            )

    generic(dargcc_bids_base,
            template_path,
            registration_mask=registration_mask,
            functional_match={'acquisition': ['EPI'], },
            structural_match={'acquisition': ['FLASH'], },
            out_base='{}/preprocessing_dargcc'.format(scratch_dir),
            workflow_name='generic',
            keep_work=config['workflow_config']['keep_work'],
            )

generic(bids_base,
        template_path,
        registration_mask=registration_mask,
        functional_match={'acquisition': ['EPIlowcov'], },
        structural_match={'acquisition': ['TurboRARElowcov'], },
        out_base='{}/preprocessing'.format(scratch_dir),
        workflow_name='masked',
        keep_work=config['workflow_config']['keep_work'],
        subjects=subjects,
        masking_config_path=config_path,
        )

generic(bids_base,
        template_path,
        registration_mask=registration_mask,
        functional_match={'acquisition': ['EPIlowcov'], },
        structural_match={'acquisition': ['TurboRARElowcov'], },
        out_base='{}/preprocessing'.format(scratch_dir),
        workflow_name='generic',
        keep_work=config['workflow_config']['keep_work'],
        subjects=subjects,
        )
