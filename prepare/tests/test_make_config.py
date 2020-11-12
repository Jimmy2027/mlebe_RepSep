import os
import tempfile
from unittest import TestCase

from make_config import prepare_config, JSON_CONFIG_PATH, \
    EXPERIMENT_RESULTS_DF_PATH


class TestMakeConfig(TestCase):
    def test_prepare_config(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            prepare_config(json_config_path=JSON_CONFIG_PATH, scratch_dir=tmpdirname,
                           experiment_results_df_path=EXPERIMENT_RESULTS_DF_PATH)
            self.assertTrue(os.path.exists(os.path.join(tmpdirname, 'config.json')))
