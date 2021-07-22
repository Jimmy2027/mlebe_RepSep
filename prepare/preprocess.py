from mlebe.masking.bids_masker import BidsMasker
from mlebe.training.configs.utils import json_to_dict
from samri.pipelines.preprocess import generic

from make_config import CONFIG_PATH as config_path, SCRATCH_DIR as scratch_dir

config = json_to_dict(config_path)

functional_match = {'acquisition': ['EPIlowcov'], }
structural_match = {'acquisition': ['TurboRARElowcov'], }

subjects = config['workflow_config']['subjects']

# mask all scans in scratch_dir / bids
# This is done before the samri pipeline such that the masking model only need to be loaded once.
bids_masker = BidsMasker(scratch_dir, str(scratch_dir / 'config.json'), structural_match=structural_match,
                         functional_match=functional_match, subjects=subjects,
                         # sessions=sessions
                         )
bids_masker.run()

# launch SAMRI preprocessing
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
        functional_match=functional_match,
        structural_match=structural_match,
        out_base='{}/preprocessing'.format(scratch_dir),
        workflow_name='masked',
        keep_work=config['workflow_config']['keep_work'],
        subjects=subjects,
        masking_config_path=config_path,
        # sessions=sessions,
        )

generic(bids_base,
        template_path,
        registration_mask=registration_mask,
        functional_match=functional_match,
        structural_match=structural_match,
        out_base='{}/preprocessing'.format(scratch_dir),
        workflow_name='generic',
        keep_work=config['workflow_config']['keep_work'],
        subjects=subjects,
        )
