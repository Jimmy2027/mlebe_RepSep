import os
import nibabel as nib
import numpy as np
from matplotlib import pyplot as plt
from mlebe.masking import utils

example = 'sub-6570_ses-4mo_acq-TurboRARE_T2w.nii.gz'
slice = 65

dir = '/mnt/data/mlebe_data/'

mask_dir = '/usr/share/mouse-brain-atlases/'

save_dir = 'Unpreprocessed/'

im_data = []
for o in os.listdir(mask_dir):
    if o == 'dsurqec_200micron_mask.nii':
        im_data.append(os.path.join(mask_dir, o))


im_data = np.sort(im_data)


for i in im_data:
    img = nib.load(i)
    mask = img.get_data()
    mask = np.moveaxis(mask, 1, 0)

for o in os.listdir(dir):
    if o != 'irsabi' and not o.startswith('.') and not o.endswith('.xz') and not o.startswith('mlebe'):
        for x in os.listdir(os.path.join(dir, o)):
            if x.endswith('preprocessing'):
                for root, dirs, files in os.walk(os.path.join(dir, o, x)):
                    for file in files:
                        if file.endswith(example):
                            img = nib.load(os.path.join(root, file))
                            img_data = img.get_data()
                            img_data = np.moveaxis(img_data, 1, 0)
                            img_data = utils.data_normalization(img_data)
                            mask = utils.arrange_mask(img_data, mask)
                            image = img_data[slice]
                            mask = mask[slice]

                            image = np.swapaxes(image, 0, 1)

                            image = np.flipud(image)
                            mask = np.swapaxes(mask, 0, 1)
                            mask = np.flipud(mask)

                            plt.imshow(np.squeeze(image), cmap='gray')
                            plt.imshow(np.squeeze(mask), alpha=0.6, cmap='Blues')
                            plt.axis('off')
                            # plt.savefig('prepro_{name}_{it}.pdf'.format(name = example ,it=slice), format='pdf')
                            # plt.close()


