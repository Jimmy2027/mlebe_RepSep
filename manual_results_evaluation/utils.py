# -*- coding: utf-8 -*-
import os
from pathlib import Path

import nibabel as nib
import numpy as np
import pandas as pd
from IPython.display import Markdown, display
from matplotlib import pyplot as plt


def printmd(string):
    # https://stackoverflow.com/questions/23271575/printing-bold-colored-etc-text-in-ipython-qtconsole
    display(Markdown(string))


def get_template_path():
    paths = [Path('/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii'),
             Path('/usr/local/share/mouse-brain-atlases/dsurqec_200micron_mask.nii')]
    for path in paths:
        if path.exists():
            return path

    raise RuntimeError(f'Template path not found under paths.')


def plot_reg_comparison():
    preprocessing_dir = Path('~/.scratch/hendrik/mlebe_threed/preprocessing').expanduser()
    generic_preprocessed_folders = preprocessing_dir / 'generic'
    template_path = get_template_path()
    template_volume = nib.load(template_path).dataobj

    m_preprocessing_dselection = pd.read_csv(preprocessing_dir / 'masked_work/data_selection.csv')

    for root, dirs, files in os.walk(generic_preprocessed_folders):
        for file in files:
            if file.endswith('.nii.gz') and 'func' not in root:

                file_path_generic = '/'.join([root, file])
                file_path_masked = '/'.join([root.replace('generic', 'masked'), file])

                p_masked_index = int(
                    m_preprocessing_dselection.loc[
                        m_preprocessing_dselection['path'].str.endswith(file), m_preprocessing_dselection.columns[
                            0]].item())
                p_masked_path = preprocessing_dir / f'masked_work/_ind_type_{p_masked_index}/s_mask/masked_output.nii.gz'

                if p_masked_path.exists():
                    masked_output = nib.load(p_masked_path).dataobj
                else:
                    masked_output = None

                printmd('# ' + file)

                volume_generic = nib.load(file_path_generic).dataobj
                volume_masked = nib.load(file_path_masked).dataobj

                for slice in range(volume_generic.shape[1]):
                    if not (np.max(volume_generic[:, slice, :]) == np.max(volume_masked[:, slice, :]) == 0):
                        plt.figure(figsize=(10, 10))
                        plt.subplot(1, 3, 1)
                        plt.title(f'Slice {slice}: Generic')
                        plt.imshow(volume_generic[:, slice, :], cmap='gray')
                        plt.imshow(template_volume[:, slice, :], alpha=0.4, cmap='Blues')
                        plt.axis('off')
                        plt.subplot(1, 3, 2)
                        plt.title(f'Slice {slice}: Masked')
                        plt.imshow(volume_masked[:, slice, :], cmap='gray')
                        plt.imshow(template_volume[:, slice, :], alpha=0.4, cmap='Blues')
                        plt.axis('off')
                        plt.subplot(1, 3, 2)
                        plt.title(f'Slice {slice}: Masked output')
                        if masked_output:
                            plt.imshow(masked_output[:, slice, :], cmap='gray')
                        plt.imshow(template_volume[:, slice, :], alpha=0.2, cmap='Blues')
                        plt.axis('off')
                        plt.show()


if __name__ == '__main__':
    print('bruh')
    plot_reg_comparison()
