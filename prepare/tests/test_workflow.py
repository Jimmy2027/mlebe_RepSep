import os
import tempfile
from unittest import TestCase

from samri.pipelines.preprocess import generic

from make_config import prepare_config, JSON_CONFIG_PATH, \
    EXPERIMENT_RESULTS_DF_PATH, prepare_experiment_result_dataframe

BIDS_BASE = '/home/hendrik/docsrc/mlebe_repsep/prepare/tests/data_for_tests'


class TestWorkflow(TestCase):
    def test_generic_masked_preprocess(self):
        """
        Tests generic masked preprocessing. Takes about 30min
        """
        # todo this test should be in SAMRI
        with tempfile.TemporaryDirectory() as tmpdirname:
            scratch_dir = tmpdirname
            print('scratch dir :', tmpdirname)
            config, workflow_uid = prepare_config(json_config_path=JSON_CONFIG_PATH, scratch_dir=scratch_dir,
                                                  experiment_results_df_path=EXPERIMENT_RESULTS_DF_PATH)
            prepare_experiment_result_dataframe(config=config, workflow_uid=workflow_uid)
            config_path = os.path.expanduser(os.path.join(scratch_dir, 'config.json'))

            generic(BIDS_BASE,
                    '/usr/share/mouse-brain-atlases/dsurqec_200micron.nii',
                    registration_mask='/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
                    functional_match={'acquisition': ['EPIlowcov'], },
                    structural_match={'acquisition': ['TurboRARElowcov'], },
                    out_base='{}/preprocessing'.format(scratch_dir),
                    workflow_name='masked',
                    model_prediction_mask=True,
                    keep_work=True,
                    subjects=['0000'],
                    masking_config_path=config_path,
                    )
            self.assertFalse(os.path.exists(os.path.join(scratch_dir, 'preprocessing/crashdump')))
            for f in ['anat/sub-0000_ses-ofM_acq-TurboRARElowcov_T2w.nii.gz',
                      'func/sub-0000_ses-ofM_task-JogB_acq-EPIlowcov_run-0_bold.nii.gz']:
                self.assertTrue(os.path.exists(os.path.join(scratch_dir, 'preprocessing/masked/sub-0000/ses-ofM', f)))
