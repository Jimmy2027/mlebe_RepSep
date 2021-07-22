# -*- coding: utf-8 -*-
import os
import tempfile
from pathlib import Path

import nibabel as nib
import numpy as np
import pandas as pd
from IPython.display import Markdown, display
from matplotlib import pyplot as plt
from nipype.interfaces.fsl.maths import MeanImage


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


def get_Tmean(in_file_path):
    with tempfile.TemporaryDirectory() as tmpdirname:
        # tMean_path = f'{tmpdirname}/tMean.nii.gz'
        tMean_path = 'tMean.nii.gz'
        mean_image = MeanImage(in_file=in_file_path, dimension='T', out_file=tMean_path)
        mean_image.run()
        mean_image = nib.load(tMean_path).dataobj
    return mean_image


def get_processed_volumes(modality: str, file_path_generic, file_path_masked):
    if modality == 'func':
        volume_generic = get_Tmean(file_path_generic)
        volume_masked = get_Tmean(file_path_masked)

    else:
        volume_generic = nib.load(file_path_generic).dataobj
        volume_masked = nib.load(file_path_masked).dataobj

    return volume_generic, volume_masked


def plot_reg_comparison(modality: str = 'func'):
    preprocessing_dir = Path('~/.scratch/hendrik/mlebe_threed/preprocessing').expanduser()
    generic_preprocessed_folders = preprocessing_dir / 'generic'
    template_path = get_template_path()
    template_volume = nib.load(template_path).dataobj

    m_preprocessing_dselection = pd.read_csv(preprocessing_dir / 'masked_work/data_selection.csv')

    for root, dirs, files in os.walk(generic_preprocessed_folders):
        for file in files:
            if file.endswith('.nii.gz') and modality in root:

                file_path_generic = '/'.join([root, file])
                file_path_masked = '/'.join([root.replace('generic', 'masked'), file])

                if (preprocessing_dir / 'masked_bids').exists():
                    d_selection = pd.read_csv(preprocessing_dir / 'masked_bids' / 'data_selection.csv')
                    p_masked_path = d_selection.loc[d_selection.path.str.endswith(file), 'masked_path'].item()
                else:
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

                volume_generic, volume_masked = get_processed_volumes(modality, file_path_generic, file_path_masked)

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
                        break


if __name__ == '__main__':
    plot_reg_comparison()
