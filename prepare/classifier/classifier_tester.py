import numpy as np
from tensorflow import keras
import os
import nibabel as nib
import pandas as pd
import pickle
import utils
import samri
from utils import dice_coef_loss, dice
import cv2
import config
from mlebe.training import unet
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

scratch_dir = os.path.expanduser(config.scratch_dir)
save_dir = scratch_dir + '/classifiers/T2'
save_dir_bin = scratch_dir + '/classifiers/T2'
path = save_dir_bin
model = keras.models.load_model(config.anat_model_path, custom_objects = {'dice_coef_loss': unet.dice_coef_loss})

xfile = open(path + '/x_test_struct.pkl', 'rb')
x_test_struct = pickle.load(xfile)
xfile.close()

yfile = open(path + '/y_test_struct.pkl', 'rb')
y_test_struct = pickle.load(yfile)
yfile.close()

x_test, x_test_affines, x_test_headers, file_names = x_test_struct['x_test'], x_test_struct['x_test_affines'], x_test_struct['x_test_headers'], x_test_struct['file_names']
y_test, y_test_affines, y_test_headers = y_test_struct['y_test'], y_test_struct['y_test_affines'], y_test_struct['y_test_headers']
shape = x_test[0][0].shape

dice_scores = []
y_pred = []

counter = 0
for x, y in zip(x_test, y_test):
    img_pred = np.empty((x.shape))
    for slice in range(x.shape[0]):
        temp = np.expand_dims(x[slice], -1)  # expand dims for channel
        temp = np.expand_dims(temp, 0)  # expand dims for batch
        prediction = model.predict(temp, verbose=0)
        prediction = np.where(np.squeeze(prediction) > 0.9, 1, 0)
        img_pred[slice, ...] = prediction
        dice_score = dice(y[slice], prediction)
        dice_scores.append(dice_score)
    counter += 1
    y_pred.append(img_pred)

np.save(save_dir_bin + '/y_test_pred', np.asarray(y_pred))
np.save(save_dir_bin + '/dice_scores_testSet', np.asarray(dice_scores))

dice_score = np.mean(dice_scores)
textfile = open(save_dir + '/dice_score.txt', 'w+')
textfile.write(str(dice_score) + '\n\n\n')
textfile.close()