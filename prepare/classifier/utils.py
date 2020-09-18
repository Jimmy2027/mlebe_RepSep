from mlebe.training.configs.utils import write_to_jsonfile
import numpy as np


def init_model_configs(config):
    anat_model_config_path = config['masking_config']['masking_config_anat']['model_config_path']
    func_model_config_path = config['masking_config']['masking_config_func']['model_config_path']

    write_to_jsonfile(anat_model_config_path,
                      [('model.use_cuda', config['masking_config']['masking_config_anat']['use_cuda'])])
    write_to_jsonfile(func_model_config_path,
                      [('model.use_cuda', config['masking_config']['masking_config_func']['use_cuda'])])


def dice(im1, im2, empty_score=1.0):
    """
    Computes the Dice coefficient, a measure of set similarity.
    Parameters
    ----------
    im1 : array-like, bool
        Any array of arbitrary size. If not boolean, will be converted.
    im2 : array-like, bool
        Any other array of identical size. If not boolean, will be converted.
    Returns
    -------
    dice : float
        Dice coefficient as a float on range [0,1].
        Maximum similarity = 1
        No similarity = 0
        Both are empty (sum eq to zero) = empty_score
    Notes
    -----
    The order of inputs for `dice` is irrelevant. The result will be
    identical if `im1` and `im2` are switched.
    """
    im1 = np.asarray(im1).astype(np.bool)
    im2 = np.asarray(im2).astype(np.bool)

    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

    im_sum = im1.sum() + im2.sum()
    if im_sum == 0:
        return empty_score

    # Compute Dice coefficient
    intersection = np.logical_and(im1, im2)
    # intersection = im1 * im2

    return 2. * intersection.sum() / im_sum
