import os
from pathlib import Path

import cv2
import numpy as np
from mlebe.training.dataio.loaders import get_dataset
from mlebe.training.dataio.loaders.utils import remove_black_images
from mlebe.training.dataio.transformation import get_dataset_transformation
from mlebe.training.models import get_model
from mlebe.training.utils.error_logger import ErrorLogger
from mlebe.training.utils.utils import json_file_to_pyobj
from mlebe.training.utils.utils import mkdir
from torch.utils.data import DataLoader
from tqdm import tqdm

from make_config import CONFIG_PATH as config_path, SCRATCH_DIR as scratch_dir

"""
This script saves x_test, y_test and y_pred as .npy files 
"""


def tester(json_opts, test_dataset, save_directory):
    model = get_model(json_opts.model)
    train_opts = json_opts.training

    test_loader = DataLoader(dataset=test_dataset, num_workers=0, batch_size=train_opts.batchSize, shuffle=False)
    error_logger = ErrorLogger()
    # test
    x_test = []
    y_test = []
    y_pred = []
    for iteration, (images, labels, indices) in tqdm(enumerate(test_loader, 1), total=len(test_loader)):
        model.set_input(images, labels)
        model.test()
        ids = test_dataset.get_ids(indices)

        stats = model.get_segmentation_stats()
        error_logger.update(stats, split='test')

        for batch_iter in range(len(ids)):
            input_arr = np.squeeze(images[batch_iter].cpu().numpy()).astype(np.float32)
            label_arr = np.squeeze(labels[batch_iter].cpu().numpy()).astype(np.int16)
            if len(ids) != 1:
                output_arr = np.squeeze(model.pred_seg.cpu().byte().numpy()).astype(np.int16)[batch_iter]
            else:
                output_arr = np.squeeze(model.pred_seg.cpu().byte().numpy()).astype(np.int16)

            y = input_arr.shape[2]
            for slice in range(y):
                if not np.max(label_arr[..., slice]) <= 0:
                    x_img = cv2.normalize(input_arr[..., slice], None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX,
                                          dtype=cv2.CV_32F)
                    assert x_img.shape == output_arr[..., slice].shape == label_arr[..., slice].shape == (
                        json_opts.augmentation.mlebe.scale_size[0], json_opts.augmentation.mlebe.scale_size[1])
                    x_test.append(x_img)
                    y_test.append(label_arr[..., slice])
                    y_pred.append(output_arr[..., slice])

    with open(os.path.join(save_directory, 'x_test.npy'), 'wb') as file1:
        np.save(file1, x_test)
    with open(os.path.join(save_directory, 'y_test.npy'), 'wb') as file2:
        np.save(file2, y_test)
    with open(os.path.join(save_directory, 'y_pred.npy'), 'wb') as file3:
        np.save(file3, y_pred)


def get_traindata(json_opts, save_directory):
    train_opts = json_opts.training
    ds_transform = get_dataset_transformation('mlebe', opts=model_json_opts.augmentation,
                                              max_output_channels=model_json_opts.model.output_nc)

    train_dataset = ds_class(template_dir, ds_path, model_json_opts.data, split='train', save_dir=None,
                             transform=ds_transform['train'],
                             train_size=split_opts.train_size, test_size=split_opts.test_size,
                             valid_size=split_opts.validation_size, split_seed=split_opts.seed,
                             training_shape=model_json_opts.augmentation.mlebe.scale_size)
    # train_loader = DataLoader(dataset=train_dataset, num_workers=16, batch_size=train_opts.batchSize, shuffle=False)
    train_loader = DataLoader(dataset=train_dataset, num_workers=0, batch_size=train_opts.batchSize, shuffle=False)

    # test
    x_train = []
    y_train = []
    for iteration, (images, labels, indices) in tqdm(enumerate(train_loader, 1), total=len(train_loader)):
        ids = train_dataset.get_ids(indices)
        for batch_iter in range(len(ids)):
            input_arr = np.squeeze(images[batch_iter].cpu().numpy()).astype(np.float32)
            label_arr = np.squeeze(labels[batch_iter].cpu().numpy()).astype(np.int16)
            input_arr, label_arr = remove_black_images(input_arr, label_arr)

            for slice in range(input_arr.shape[-1]):
                if not np.max(label_arr[..., slice]) <= 0:
                    x_train.append(
                        cv2.normalize(input_arr[..., slice], None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX,
                                      dtype=cv2.CV_32F))
                    y_train.append(label_arr[..., slice])

    with open(os.path.join(save_directory, 'x_train.npy'), 'wb') as file1:
        np.save(file1, x_train)
    with open(os.path.join(save_directory, 'y_train.npy'), 'wb') as file2:
        np.save(file2, y_train)


save_dir = os.path.expanduser(os.path.join(scratch_dir, 'classifiers', 'T2'))
mkdir(save_dir)

workflow_json_opts = json_file_to_pyobj(config_path)
model_config_path = Path(
    workflow_json_opts.masking_config.masking_config_anat.model_folder_path) / 'trained_mlebe_config_anat.json'
model_json_opts = json_file_to_pyobj(model_config_path)
data_dir = model_json_opts.data.data_dir
template_dir = '/usr/share/mouse-brain-atlases/'

ds_class = get_dataset('mlebe_dataset')
ds_path = model_json_opts.data.data_dir
channels = model_json_opts.data_opts.channels
split_opts = model_json_opts.data_split
train_opts = model_json_opts.training
ds_transform = get_dataset_transformation('mlebe', opts=model_json_opts.augmentation,
                                          max_output_channels=model_json_opts.model.output_nc)

test_dataset = ds_class(template_dir, ds_path, model_json_opts.data, split='test', save_dir=None,
                        transform=ds_transform['valid'],
                        train_size=split_opts.train_size, test_size=split_opts.test_size,
                        valid_size=split_opts.validation_size, split_seed=split_opts.seed,
                        training_shape=model_json_opts.augmentation.mlebe.scale_size[:3])

tester(model_json_opts, test_dataset, save_dir)
# get_traindata(model_json_opts, save_dir)#
