import os
from shutil import copyfile
import numpy as np
from make_config import config_path, scratch_dir
from mlebe.threed.training.dataio.loaders import get_dataset
from mlebe.threed.training.dataio.transformation import get_dataset_transformation
from mlebe.threed.training.models import get_model
from mlebe.threed.training.utils.utils import json_file_to_pyobj
from mlebe.threed.training.utils.utils import mkdir
from mlebe.training.utils.general import remove_black_images
from torch.utils.data import DataLoader
from tqdm import tqdm


def tester(json_opts, test_dataset, save_directory):
    model = get_model(json_opts.model)
    train_opts = json_opts.training

    test_loader = DataLoader(dataset=test_dataset, num_workers=16, batch_size=train_opts.batchSize, shuffle=False)

    # test
    x_test = []
    y_test = []
    y_pred = []
    for iteration, (images, labels, indices) in tqdm(enumerate(test_loader, 1), total=len(test_loader)):
        model.set_input(images, labels)
        model.test()
        ids = test_dataset.get_ids(indices)

        for batch_iter in range(len(ids)):
            input_arr = np.squeeze(images[batch_iter].cpu().numpy()).astype(np.float32)
            label_arr = np.squeeze(labels[batch_iter].cpu().numpy()).astype(np.int16)
            if not len(ids) == 1:
                output_arr = np.squeeze(model.pred_seg.cpu().byte().numpy()).astype(np.int16)[batch_iter]
            else:
                output_arr = np.squeeze(model.pred_seg.cpu().byte().numpy()).astype(np.int16)

            input_img, target = remove_black_images(input_arr, label_arr)
            _, output_img = remove_black_images(input_arr, output_arr)

            y = input_img.shape[2]
            for slice in range(y):
                x_test.append(input_img[..., slice])
                y_test.append(target[..., slice])
                y_pred.append(output_img[..., slice])

    with open(os.path.join(save_directory, 'x_test.npy'), 'wb') as file1:
        np.save(file1, x_test)
    with open(os.path.join(save_directory, 'y_test.npy'), 'wb') as file2:
        np.save(file2, y_test)
    with open(os.path.join(save_directory, 'y_pred.npy'), 'wb') as file3:
        np.save(file3, y_pred)


save_dir = os.path.expanduser(os.path.join(scratch_dir, 'classifiers', 'T2'))
mkdir(save_dir)
# get blacklisted slices
copyfile('/home/hendrik/.scratch/mlebe_final/classifiers/T2/blacklisted_images.pkl',
         os.path.join(save_dir, 'blacklisted_images.pkl'))
copyfile('/home/hendrik/.scratch/mlebe_final/classifiers/T2/blacklisted_masks.pkl',
         os.path.join(save_dir, 'blacklisted_masks.pkl'))

workflow_json_opts = json_file_to_pyobj(config_path)
model_json_opts = json_file_to_pyobj(workflow_json_opts.masking_config.masking_config_anat.model_config_path)
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
