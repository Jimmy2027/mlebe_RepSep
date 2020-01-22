import numpy as np
from tensorflow import keras
import os
import nibabel as nib
import pickle
from matplotlib import pyplot as plt
import utils
import cv2
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

def dice_coef(y_true, y_pred, smooth=1):
    import tensorflow.keras.backend as K
    """
    Dice = (2*|X & Y|)/ (|X|+ |Y|)
         =  2*sum(|A*B|)/(sum(A)+sum(B))
    ref: https://arxiv.org/pdf/1606.04797v1.pdf
    """
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)

    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)

def dice_coef_loss(y_true, y_pred):
    return 1-dice_coef(y_true, y_pred)


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


remote = False
loss = 'dice'
slice_view = 'coronal'


path = 'data/dice_600_2019-12-18'
save_dir = 'mlebe_figs/'
model_dir = path + '/1_Step/unet_ep381_val_loss0.05.hdf5'


if loss == 'dice':
    model = keras.models.load_model(model_dir, custom_objects = {'dice_coef_loss': dice_coef_loss})
elif loss == 'bincross':
    model = keras.models.load_model(model_dir)
else: print('wrong loss function defined')

shape = (64, 64)


xfile = open(path + '/x_test_struct.pkl', 'rb')
x_test_struct = pickle.load(xfile)
xfile.close()

yfile = open(path + '/y_test_struct.pkl', 'rb')
y_test_struct = pickle.load(yfile)
yfile.close()

x_test, x_test_affines, x_test_headers, file_names = x_test_struct['x_test'], x_test_struct['x_test_affines'], x_test_struct['x_test_headers'], x_test_struct['file_names']
y_test, y_test_affines, y_test_headers = y_test_struct['y_test'], y_test_struct['y_test_affines'], y_test_struct['y_test_headers']


x_test = [x_test[3]]
y_test = [y_test[3]]
x_test = [i[1::12] for i in x_test]
y_test = [i[1::12] for i in y_test]

y_pred = []   #predictions of the test set
dice_scores_string = []
dice_scores = []
dice_scores_thr = []
for i in y_test:
    img_pred = np.empty((i.shape))
    dice_score_img = []
    dice_score_img_thr = []
    for slice in range(i.shape[0]):
        temp = np.expand_dims(i[slice], -1)  # expand dims for channel
        temp = np.expand_dims(temp, 0)  # expand dims for batch
        prediction = model.predict(temp, verbose=0)
        prediction = np.squeeze(prediction)
        img_pred[slice, ...] = prediction
        dice_scores.append(dice(i[slice], prediction))
        dice_score_img.append('dice: ' + str(np.round(dice(i[slice], prediction), 3)))
        dice_score_img_thr.append('dice: ' + str(np.round(dice(np.where(np.squeeze(i[slice]) > 0.9, 1, 0), prediction), 3)))

    y_pred.append(img_pred)
    dice_scores_string.append(dice_score_img)
    dice_scores_thr.append(dice_score_img_thr)

temp = np.concatenate(y_pred, 0)
dice_score = np.median(dice_scores)


thresholds = [0]
outputs = []
slice_titles = [None, None, dice_scores_string, None]
row_titles = ['x_test']

corr_temp = [utils.corr(y, x) for x, y in zip(x_test, y_test)]

row_titles.append('y_test' + '\n corr: ' + str(np.round(np.median(corr_temp),3)))
correlations_thr = []

for thr in thresholds:
    if thr == 0:
        outputs.append([np.squeeze(img) for img in y_pred])
        dice_temp = [dice(np.squeeze(img), y_true) for img, y_true in zip(y_pred,y_test)]
        corr_temp = [utils.corr(img, x) for img, x in zip(y_pred, x_test)]
        row_titles.append('Prediction \n' + 'Dice: ' + str(np.round(np.median(dice_temp), 3)) + '\n corr: ' + str(np.round(np.median(corr_temp),3)))
    else:
        outputs.append([np.where(np.squeeze(img) > thr, 1, 0) for img in y_pred])
        dice_temp = [dice(np.where(np.squeeze(img) > thr, 1, 0), y_true) for img, y_true in zip(y_pred, y_test)]
        corr_temp = [utils.corr(np.where(img > thr, 1, 0), x) for img, x in zip(y_pred, x_test)]

        row_titles.append('thr: ' + str(thr) + '\n ' + 'Dice: ' + str(np.round(np.median(dice_temp), 3)) + '\n corr: ' + str(np.round(np.median(corr_temp),3)))

utils.compute_correlation(np.concatenate(x_test), np.concatenate(y_test),np.concatenate(outputs[0]), save_dir)

list = [[x_test[0][:4]], [y_test[0][:4]]]
for o in outputs:
    list.append([o[0][:4]])
slice_titles[-1] = dice_scores_thr



utils.save_datavisualisation_plt(list, save_dir, normalized=True, file_names=file_names, slice_titles=slice_titles, row_titles=row_titles)

dice_score = np.median(dice_scores)
print('median Dice score: ', dice_score)


# np.save(save_dir + 'y_pred_{}dice'.format(np.round(dice_score, 4)), y_pred)


