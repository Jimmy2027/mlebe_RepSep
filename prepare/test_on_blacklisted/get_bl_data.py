from mlebe.training import utils
import os

data_dir = '/mnt/data/mlebe_data/'
data_sets = ['drlfom', 'mgtdbs', 'opfvta', 'ztau']
blacklist = utils.write_blacklist('../data/Blacklist')
bids_dir = os.path.expanduser('~/.scratch/mlebe/bids/')


for o in os.listdir(data_dir):
    if o in data_sets:
        print(o)
        for x in os.listdir(os.path.join(data_dir, o)):
            if x.endswith('bids') and not x.startswith('_'):
                for root, dirs, files in os.walk(os.path.join(data_dir, o, x)):
                    for file in files:
                        if file.endswith("_T2w.nii.gz"):
                            for i in blacklist:
                                if file.startswith('sub-' + i.subj + '_ses-' + i.sess + '_'):
                                    print('root', root)
                                    split = root.split('/')
                                    file = '/'.join(split[:-1])
                                    subject = split[-3]
                                    if not os.path.exists(os.path.join(bids_dir, subject)):
                                        os.mkdir(os.path.join(bids_dir, subject))
                                    print(subject)
                                    command = 'cp -r {} {}'.format(file, os.path.join(bids_dir, subject))
                                    # os.system(command)
                                    print(command)