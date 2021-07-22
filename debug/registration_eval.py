import glob

import ants
from mlebe.training.configs.utils import json_to_dict

from register_grid_search import *


class RegistrationEval:
    def __init__(self, preprocessing_dir: Path):
        self.preprocessing_dir = preprocessing_dir
        self.df = pd.DataFrame()

    def run_eval(self):
        for method in ['masked', 'generic']:
            work_dir = self.preprocessing_dir / f"{method}_work"
            for dir in work_dir.iterdir():
                if dir.name.startswith('_ind_'):
                    transform_path = dir / 's_register' / 'output_'
                    warp_config = json_to_dict(glob.glob(str(dir / 's_warp' / '*.json'))[0])
                    bids_path = [k[1] for k in warp_config if k[0] == 'input_image'][0][0]
                    subject = [k[1] for k in warp_config if k[0] == 'output_image'][0]

                    out_dir = Path(subject) / method
                    out_dir.mkdir(exist_ok=True, parents=True)

                    if method == 'masked':
                        mask_path = dir / 's_mask' / 'resampled_mask.nii.gz'
                    else:
                        mask_path = Path(
                            self.df.loc[(self.df['subject'] == subject) & (
                                        self.df['method'] == 'masked'), 'mask_path'].tolist()[0])

                    # transform mask:
                    transformed_mask_path = out_dir / 'transformed_mask.nii.gz'
                    apply_transform(mask_path, transform_path, transformed_mask_path)

                    # Evaluation
                    tf_mask_data = ants.image_read(str(transformed_mask_path)).numpy()
                    template_mask_data = ants.image_read(str(TEMPLATE_MASK_PATH)).numpy()

                    dice_score = dice(tf_mask_data, template_mask_data)

                    self.df = self.df.append(
                        {'method': method, 'dice_score': dice_score, 'subject': subject, '_ind': dir.name,
                         'mask_path': mask_path, 'bids_path': bids_path},
                        ignore_index=True)


if __name__ == '__main__':
    reg_eval = RegistrationEval(Path('/home/hendrik/.scratch/hendrik/mlebe/preprocessing'))
    reg_eval.run_eval()
    reg_eval.df.to_csv('reg_eval.csv', index=False)
