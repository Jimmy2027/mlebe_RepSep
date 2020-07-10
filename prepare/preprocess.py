from make_config import config_path, scratch_dir
from mlebe.training.three_D.configs.utils import json_to_dict
from samri.pipelines.preprocess import generic

config = json_to_dict(config_path)
subjects = config['workflow_config']['subjects']
bids_base = '{}/bids'.format(scratch_dir)

# Preprocess all of the data:
if config['workflow_config']['with_FLASH']:
        # todo does it make sense to have a separate folder for this?
    dargcc_bids_base = '{}/dargcc_bids'.format(scratch_dir)

    generic(dargcc_bids_base,
            '/usr/share/mouse-brain-atlases/dsurqec_200micron.nii',
            registration_mask='/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
            functional_match={'acquisition': ['EPI'], },
            structural_match={'acquisition': ['FLASH'], },
            out_base='{}/preprocessing_dargcc'.format(scratch_dir),
            workflow_name='masked',
            model_prediction_mask=True,
            keep_work=True,
            masking_config_path=config_path,
            )

    generic(dargcc_bids_base,
            '/usr/share/mouse-brain-atlases/dsurqec_200micron.nii',
            registration_mask='/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
            functional_match={'acquisition': ['EPI'], },
            structural_match={'acquisition': ['FLASH'], },
            out_base='{}/preprocessing_dargcc'.format(scratch_dir),
            workflow_name='generic',
            keep_work=True,
            )

generic(bids_base,
        '/usr/share/mouse-brain-atlases/dsurqec_200micron.nii',
        registration_mask='/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
        functional_match={'acquisition': ['EPIlowcov'], },
        structural_match={'acquisition': ['TurboRARElowcov'], },
        out_base='{}/preprocessing'.format(scratch_dir),
        workflow_name='masked',
        model_prediction_mask=True,
        keep_work=True,
        subjects=subjects,
        masking_config_path=config_path,
        )

generic(bids_base,
        '/usr/share/mouse-brain-atlases/dsurqec_200micron.nii',
        registration_mask='/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
        functional_match={'acquisition': ['EPIlowcov'], },
        structural_match={'acquisition': ['TurboRARElowcov'], },
        out_base='{}/preprocessing'.format(scratch_dir),
        workflow_name='generic',
        keep_work=True,
        subjects=subjects,
        )
