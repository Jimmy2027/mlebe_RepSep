# -*- coding: utf-8 -*-
from pathlib import Path

from smoothness_data import avg_smoothness
from tests.test_workflow import init_test_data


def test_avg_smoothness():
    init_test_data()
    avg_smoothness(inp_file=Path(
        __file__).parent / 'data_for_tests/bids_collapsed/sub-0000/ses-ofM/func/sub-0000_ses-ofM_task-JogB_acq-EPIlowcov_run-0_bold.nii.gz')


if __name__ == '__main__':
    test_avg_smoothness()
