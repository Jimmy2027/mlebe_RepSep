import config_3D
from samri.pipelines.preprocess import generic
from subjects_reader import find_subjects

scratch_dir = '~/.scratch/mlebe'
subjects = find_subjects()
bids_base = '{}/bids'.format(scratch_dir)
import samri

print(samri.__file__)
# Preprocess all of the data:

if not config_3D.parameters['with_FLASH_train']:
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
                classifier_paths=[config_3D.anat_model_path, config_3D.func_model_path],
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
        # subjects= subjects,
        classifier_paths=[config_3D.anat_model_path, config_3D.func_model_path],
        )

generic(bids_base,
        '/usr/share/mouse-brain-atlases/dsurqec_200micron.nii',
        registration_mask='/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
        functional_match={'acquisition': ['EPIlowcov'], },
        structural_match={'acquisition': ['TurboRARElowcov'], },
        out_base='{}/preprocessing'.format(scratch_dir),
        workflow_name='generic',
        keep_work=True,
        # subjects= subjects,
        )
