# -*- coding: utf-8 -*-
import os
import tempfile
from pathlib import Path
from unittest import TestCase

from samri.pipelines import glm
from samri.pipelines import manipulations
from samri.pipelines.preprocess import generic

from make_config import prepare_config, prepare_experiment_result_dataframe

TEST_DATA_DIR = Path(os.getcwd()) / 'tests/data_for_tests'
BIDS_BASE = TEST_DATA_DIR / 'bids'
JSON_CONFIG_PATH = Path(os.getcwd()) / 'configs/test_config.json'


def init_test_data():
    """
    If test_data doesn't exists, downloads it and extracts it.
    """
    bids_base = Path(BIDS_BASE)
    if not bids_base.exists():
        with tempfile.TemporaryDirectory() as tmpdirname:
            zip_name = '123222caf93a.zip'
            # zip_name = 'a6e69f24ee84.zip'
            wget_command = f'wget https://ppb.hendrikklug.xyz/{zip_name} -P {tmpdirname}/'
            print(wget_command)
            os.system(wget_command)
            unzip_command = f'unzip {tmpdirname}/{zip_name} -d {Path(__file__).parent}/'
            os.system(unzip_command)
    assert bids_base.exists()


class TestWorkflow(TestCase):
    """Tests for the preprocessing workflow."""

    def test_generic_masked_preprocess(self):
        """
        Tests generic masked preprocessing. Takes about 30min
        """
        # todo this test should be in SAMRI
        init_test_data()
        with tempfile.TemporaryDirectory() as tmpdirname:
            scratch_dir = Path(tmpdirname)
            print('scratch dir :', tmpdirname)

            config, workflow_uid = prepare_config(json_config_path=JSON_CONFIG_PATH, scratch_dir=scratch_dir)
            prepare_experiment_result_dataframe(config=config, workflow_uid=workflow_uid)
            config_path = os.path.expanduser(os.path.join(scratch_dir, 'config.json'))

            generic(BIDS_BASE,
                    '/usr/share/mouse-brain-atlases/dsurqec_200micron.nii',
                    registration_mask='/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
                    functional_match={'acquisition': ['EPIlowcov'], },
                    structural_match={'acquisition': ['TurboRARElowcov'], },
                    out_base='{}/preprocessing'.format(scratch_dir),
                    workflow_name='masked',
                    keep_work=False,
                    subjects=['0000'],
                    masking_config_path=config_path,
                    )
            assert not os.path.exists(os.path.join(scratch_dir, 'preprocessing/crashdump'))
            for f in ['anat/sub-0000_ses-ofM_acq-TurboRARElowcov_T2w.nii.gz',
                      'func/sub-0000_ses-ofM_task-JogB_acq-EPIlowcov_run-0_bold.nii.gz']:
                out_path = os.path.exists(os.path.join(scratch_dir, 'preprocessing/masked/sub-0000/ses-ofM', f))
                assert out_path, f'Test failed, path {out_path} does not exist.'
        print('finished test_generic_masked_preprocess successfully.')

    def test_generic_preprocess(self):
        """
        Tests generic preprocessing. Takes about 30min
        """
        init_test_data()
        with tempfile.TemporaryDirectory() as tmpdirname:
            scratch_dir = Path(tmpdirname)
            print('scratch dir :', tmpdirname)
            args = [(f'masking_config.masking_config_{mod}.visualisation_path', str(scratch_dir / f'vis_{mod}')) for mod in
                    ['anat', 'func']]
            config, workflow_uid = prepare_config(json_config_path=JSON_CONFIG_PATH, scratch_dir=scratch_dir,
                                                  additional_args=args)
            prepare_experiment_result_dataframe(config=config, workflow_uid=workflow_uid)
            config_path = os.path.expanduser(os.path.join(scratch_dir, 'config.json'))

            generic(BIDS_BASE,
                    '/usr/share/mouse-brain-atlases/dsurqec_200micron.nii',
                    registration_mask='/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
                    functional_match={'acquisition': ['EPIlowcov'], },
                    structural_match={'acquisition': ['TurboRARElowcov'], },
                    out_base='{}/preprocessing'.format(scratch_dir),
                    workflow_name='generic',
                    keep_work=False,
                    subjects=['0000'],
                    masking_config_path=config_path,
                    )
            assert not os.path.exists(os.path.join(scratch_dir, 'preprocessing/crashdump'))
            for f in ['anat/sub-0000_ses-ofM_acq-TurboRARElowcov_T2w.nii.gz',
                      'func/sub-0000_ses-ofM_task-JogB_acq-EPIlowcov_run-0_bold.nii.gz']:
                out_path = os.path.exists(os.path.join(scratch_dir, 'preprocessing/generic/sub-0000/ses-ofM', f))
                assert out_path, f'Test failed, path {out_path} does not exist.'
        print('finished test_generic_preprocess successfully.')

    def test_collapse_bids(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            bids_base = BIDS_BASE
            manipulations.collapse_nifti(in_dir=bids_base,
                                         out_dir='{}/bids_collapsed'.format(tmpdirname),
                                         )
        print('finished test_collapse_bids successfully.')

    def test_collapse_masked(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            os.mkdir(f'{tmpdirname}/peprocessing')
            manipulations.collapse_nifti('{}/preprocessing/masked'.format(TEST_DATA_DIR),
                                         '{}/preprocessing/masked_collapsed'.format(tmpdirname),
                                         )
        print('finished test_collapse_masked successfully.')

    def test_collapse_generic(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            os.mkdir(f'{tmpdirname}/peprocessing')
            manipulations.collapse_nifti('{}/preprocessing/generic'.format(TEST_DATA_DIR),
                                         '{}/preprocessing/generic_collapsed'.format(tmpdirname),
                                         )

    def test_l1_masked(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            workflow_name = 'masked'
            mask = '/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii'
            preprocess_base = '{}/preprocessing/'.format(TEST_DATA_DIR)
            bf_path = TEST_DATA_DIR / 'chr_beta1.txt'

            glm.l1(os.path.join(preprocess_base, workflow_name),
                   bf_path=bf_path,
                   workflow_name=workflow_name,
                   habituation="confound",
                   mask=mask,
                   keep_work=False,
                   match={'suffix': ['bold']},
                   exclude={'task': ['rest']},
                   invert=False,
                   out_base='{}/l1'.format(tmpdirname)
                   )
        print('finished test_l1_masked successfully.')

    def test_l1_generic(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            workflow_name = 'generic'
            mask = '/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii'
            preprocess_base = '{}/preprocessing/'.format(TEST_DATA_DIR)
            bf_path = TEST_DATA_DIR / 'chr_beta1.txt'

            glm.l1(os.path.join(preprocess_base, workflow_name),
                   bf_path=bf_path,
                   workflow_name=workflow_name,
                   habituation="confound",
                   mask=mask,
                   keep_work=False,
                   match={'suffix': ['bold']},
                   exclude={'task': ['rest']},
                   invert=False,
                   out_base='{}/l1'.format(tmpdirname)
                   )
        print('finished test_l1_generic successfully.')


if __name__ == '__main__':
    from norby.utils import norby

    with norby('starting mlebe test workflow', 'mlebe test workflow finished.'):
        TestWorkflow.test_generic_preprocess(TestWorkflow)
        TestWorkflow.test_generic_masked_preprocess(TestWorkflow)
        TestWorkflow.test_collapse_bids(TestWorkflow)
        TestWorkflow.test_collapse_generic(TestWorkflow)
        TestWorkflow.test_collapse_masked(TestWorkflow)
        TestWorkflow.test_l1_generic(TestWorkflow)
        TestWorkflow.test_l1_masked(TestWorkflow)
