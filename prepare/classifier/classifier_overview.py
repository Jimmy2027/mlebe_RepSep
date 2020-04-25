import pandas as pd
import json
import os
from mlebe.training.utils.masking_vis import tester
from matplotlib import pyplot as plt
import operator, functools
import numpy as np
experiment_config = '/Users/Hendrik/Desktop/bartholin/results/attention_unet_anat/dice_600_2020-04-21/1_Step/experiment_config.json'
vis_dir = '/Users/Hendrik/Desktop/bartholin/results/attention_unet_anat/dice_600_2020-04-21/1_Step'
# experiment_config = '/mnt/data/mlebe_data/results/attention_unet_anat/dice_600_2020-04-21/1_Step/experiment_config.json'
# vis_dir = '/mnt/data/mlebe_data/results/attention_unet_anat/dice_600_2020-04-21/1_Step'
results_df = 'results_df.csv'

with open(experiment_config) as json_file:
    experiment_config = json.load(json_file)

if os.path.isfile(results_df):
    results_df = pd.read_csv(results_df)
else:
    columns = ['good', 'bad', 'okay']
    for key in experiment_config.keys():
        columns.append(key)
    results_df = pd.DataFrame(columns=columns)

if not os.path.isdir(vis_dir):
    tester(os.path.expanduser('/usr/share/'), ['irsabi_bidsdata'], vis_dir, experiment_config['model_path'],
           data_type='anat', visualisation_format='png')

labels_df = os.path.join(vis_dir, 'labels_df.csv')
if not os.path.isfile(labels_df):
    labels_df = pd.DataFrame(columns=['subject', 'slice', 'label'])
else:
    labels_df = pd.read_csv(labels_df)

def get_label(labels_df,slice, rewind = False):
    img_path = os.path.join(vis_dir, 'anat', dir, slices[slice])
    temp_df = labels_df.loc[functools.reduce(operator.and_, (labels_df[item] == current for item, current in
                                                             zip(['subject', 'slice'], [dir, int(slice)]))), 'label']
    if temp_df.empty or temp_df.isna().all() or rewind or not (temp_df.values.all() in ['good', 'bad', 'okay']):
        plot = plt.imread(img_path)
        plt.imshow(plot)
        plt.title(slice)
        plt.show(block=False)
        label = input('Good or bad?')
        if label in ['', 'q']:
            label = 'good'
        elif label in ['w', 'b']:
            label = 'bad'
        elif label in ['o']:
            label = 'okay'
        elif label == '-':
            label = label
        else:
            raise Exception('wrong input')
        plt.clf()
        plt.close()

        return label

    else:
        print('already seen')
        return 'seen'

for idx, dir in enumerate(os.listdir(os.path.join(vis_dir, 'anat'))):
    print(idx, ' out of ', len(os.listdir(os.path.join(vis_dir, 'anat'))))
    if os.path.isdir(os.path.join(vis_dir, 'anat',dir)):
        slices = os.listdir(os.path.join(vis_dir, 'anat',dir))
        for slice in range(len(slices)):
            slice_temp = 0
            label = get_label(labels_df, slice)
            print('label = ', label)
            while (label == '-' and slice-slice_temp > 0):
                slice_temp += 1
                label = get_label(labels_df, slice-slice_temp, rewind=True)
            while slice_temp > 0:
                slice_temp = slice_temp -1
                label = get_label(labels_df, slice-slice_temp, rewind=True)
            if not label == 'seen':
                labels_df = labels_df.append({'subject': dir, 'slice': slice, 'label': label}, ignore_index=True)
                labels_df.to_csv(os.path.join(vis_dir, 'labels_df.csv'), index=False)

total_good = len(labels_df.loc[labels_df['label'] == 'good'].values.tolist())
total_bad = len(labels_df.loc[labels_df['label'] == 'bad'].values.tolist())
total_okay = len(labels_df.loc[labels_df['label'] == 'okay'].values.tolist())

temp = experiment_config
temp['good'] = total_good
temp['bad'] = total_bad
temp['okay'] = total_okay
results_df = results_df.append(temp, ignore_index=False)
results_df.to_csv('results_df.csv')