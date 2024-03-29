import os
import pandas as pd

data_dir = '/mnt/data/mlebe_data/'
bids_dir = os.path.expanduser('~/.scratch/mlebe/bids/')

blacklist_df = pd.read_csv('blacklist.csv')
blacklist_df = blacklist_df.loc[blacklist_df['label'] == 'bad']
counts_df = blacklist_df.groupby(['study', 'subject', 'session', 'acquisition', 'modality']).count()
scan = pd.DataFrame([counts_df.loc[counts_df['slice'] == counts_df['slice'].max()].index.values[0]], columns=['study', 'subject', 'session', 'acquisition', 'modality'])

for o in os.listdir(data_dir):
    if o == scan['study'].values[0]:
        print(o)
        for x in os.listdir(os.path.join(data_dir, o)):
            if x.endswith('bids') and not x.startswith('_'):
                for root, dirs, files in os.walk(os.path.join(data_dir, o, x)):
                    for file in files:
                        if file.endswith("_T2w.nii.gz"):
                            if file.startswith('sub-' + str(scan['subject'].values[0]) + '_ses-' + scan['session'].values[0] + '_'):
                                print('root', root)
                                split = root.split('/')
                                file = '/'.join(split[:-1])
                                subject = split[-3]
                                # if not os.path.exists(os.path.join(bids_dir, subject)):
                                #     os.mkdir(os.path.join(bids_dir, subject))
                                print(subject)
                                command = 'cp -r {} {}'.format(file, os.path.join(bids_dir, subject))
                                # os.system(command)
                                print(command)