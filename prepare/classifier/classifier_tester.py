import mlebe.training.utils.data_loader as dl
import mlebe.training.utils.general as utils
import mlebe.training.utils.scoring_utils as su
import copy
from mlebe.training import unet
from tensorflow import keras
import config
import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
data_dir = config.data_path
template_dir = '/usr/share/mouse-brain-atlases/'
study = ['irsabi']
slice_view = 'coronal'
shape = (128, 128)
IMG_NBRs = [65, 65, 65, 65, 65, 65, 65, 65]


def evaluate(data_type):
    if data_type == 'anat':
        excluded_img_data = dl.load_img(data_dir, studies=study)
        model = keras.models.load_model(config.func_model_path, custom_objects={'dice_coef_loss': unet.dice_coef_loss,
                                                                                'dice_coef': unet.dice_coef})
        save_path = config.anat_model_path.split('/')

    else:
        excluded_img_data = dl.load_func_img(data_dir, studies=study)
        model = keras.models.load_model(config.func_model_path, custom_objects={'dice_coef_loss': unet.dice_coef_loss,
                                                                                'dice_coef': unet.dice_coef})
        save_path = config.func_model_path.split('/')

    save_path[-1] = 'irsabi_test'
    save_path = '/'.join(save_path)
    print(save_path)
    mask_data = []
    temp = dl.load_mask(template_dir)
    for i in range(len(excluded_img_data)):
        mask_data.append(copy.deepcopy(temp[0]))

    img_data, mask_data, img_affines, img_headers, img_file_names, mask_affines, mask_headers = utils.get_image_and_mask(
        '', excluded_img_data, mask_data, shape, '', slice_view=slice_view,
        visualisation=False, blacklist_bool=False)

    dice_scores_df = pd.DataFrame(columns=['volume_name', 'slice', 'dice_score', 'idx'])
    predictions = []
    for volume in range(len(img_data)):
        volume_name = img_file_names[volume]
        predicted_volume = np.empty(img_data[volume].shape)
        for slice in range(img_data[volume].shape[0]):
            prediction = np.squeeze(model.predict(np.expand_dims(np.expand_dims(img_data[volume][slice], 0), -1)))
            prediction = np.where(prediction > 0.9, 1, 0)
            predicted_volume[slice] = prediction
            dice_score = su.dice(mask_data[volume][slice], prediction)
            dice_scores_df = dice_scores_df.append(
                {'volume_name': volume_name, 'slice': slice, 'dice_score': dice_score, 'idx': volume},
                ignore_index=True)
        predictions.append(predicted_volume)

    min_df = dice_scores_df.sort_values(by=['dice_score']).head(sum(IMG_NBRs))
    df_idx = 0
    with PdfPages('../data/irsabi_test_{}.pdf'.format(data_type)) as pdf:
        for IMG_NBR in IMG_NBRs:
            plt.figure(figsize=(40, IMG_NBR * 10))
            plt.figtext(.5, .9, 'Mean dice score of {}'.format(np.round(dice_scores_df['dice_score'].mean(), 4)),
                        fontsize=100, ha='center')
            i = 1
            while i <= IMG_NBR * 2:
                volume = min_df.iloc[df_idx]['idx']
                slice = min_df.iloc[df_idx]['slice']
                dice_score = min_df.iloc[df_idx]['dice_score']
                plt.subplot(IMG_NBR, 2, i)
                plt.imshow(img_data[volume][slice], cmap='gray')
                plt.imshow(mask_data[volume][slice], cmap='Blues', alpha=0.6)
                plt.axis('off')
                i += 1
                plt.subplot(IMG_NBR, 2, i)
                plt.imshow(img_data[volume][slice], cmap='gray')
                plt.imshow(predictions[volume][slice], cmap='Blues', alpha=0.6)
                plt.title('Volume: {}, slice {}, dice {}'.format(img_file_names[volume], slice, dice_score))
                plt.axis('off')
                i += 1
                df_idx += 1
            pdf.savefig()
            plt.close()

    plt.title('Dice score = {}'.format(dice_scores_df['dice_score'].mean()))
    plt.savefig('{}.pdf'.format(save_path), format='pdf')

    df = pd.DataFrame([[]])
    df['irsabi_dice_{}'.format(data_type)] = dice_scores_df['dice_score'].mean()
    df['irsabi_dice_std_{}'.format(data_type)] = dice_scores_df['dice_score'].std()
    df['uid'] = config.uid
    reg_results = pd.read_csv('classifier/reg_results.csv')
    reg_results = pd.concat([reg_results, df]).groupby('uid', as_index=False).first()
    reg_results.to_csv('classifier/reg_results.csv', index=False)

    if os.path.exists(config.anat_model_training_config):
        models_results = pd.read_csv('classifier/results_df.csv')
        if data_type == 'anat':
            anat_model_training_config = pd.read_csv(config.anat_model_training_config)
            df['uid'] = anat_model_training_config['uid']
        elif data_type == 'func':
            func_model_training_config = pd.read_csv(config.func_model_training_config)
            df['uid'] = func_model_training_config['uid']
        models_results = pd.concat([models_results, df]).groupby('uid', as_index=False).first()
        models_results.to_csv('classifier/results_df.csv', index=False)

    command = 'cp ../data/irsabi_test_{}.pdf {}.pdf'.format(data_type, save_path)
    print(command)
    os.system(command)


evaluate('anat')
evaluate('func')
