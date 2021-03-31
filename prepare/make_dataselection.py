"""Creates a dataselection dataframe."""

import os

import pandas as pd
from mlebe.training.configs.utils import json_to_dict

from make_config import CONFIG_PATH as config_path

config = json_to_dict(config_path)
data_dir = config['workflow_config']['data_path']
studies = ["drlfom", "mgtdbs", "opfvta", "ztau", "hendrik_nvcz", 'irsabi']


def make_dataselection_anat(data_dir, studies):
    data_selection = pd.DataFrame()
    for o in os.listdir(data_dir):
        if (not studies or o in studies) and not o.startswith('.') and not o.endswith(
                '.xz'):  # i.e. if o in studies or if studies empty
            data_set = o
            for x in os.listdir(os.path.join(data_dir, o)):
                if (x.endswith('preprocessed') or x.startswith('preprocess') or x.endswith(
                        'preprocessing')) and not x.endswith('work'):
                    for root, dirs, files in os.walk(os.path.join(data_dir, o, x)):
                        for file in files:
                            if not file.startswith('.') and (
                                    file.endswith("_T2w.nii.gz") or file.endswith("_T1w.nii.gz")):
                                split = file.split('_')
                                subject = split[0].split('-')[1]
                                session = split[1].split('-')[1]
                                acquisition = split[2].split('-')[1]
                                type = split[3].split('.')[0]
                                uid = file.split('.')[0]
                                path = os.path.join(root, file)

                                data_selection = pd.concat([data_selection, pd.DataFrame(
                                    [[data_set, subject, session, acquisition, type, uid, path]],
                                    columns=['data_set', 'subject', 'session', 'acquisition', 'type', 'uid',
                                             'path'])]).reset_index(drop=True)

    return data_selection


def make_dataselection_func(data_dir, studies):
    data_selection = pd.DataFrame()

    for o in os.listdir(data_dir):
        if o in studies and not o.startswith('.') and not o.startswith('.') and not o.endswith('.xz'):
            data_set = o
            for x in os.listdir(os.path.join(data_dir, o)):
                if (x.endswith('preprocessed') or x.startswith('preprocess') or x.endswith(
                        'preprocessing')) and not x.endswith('work'):
                    for root, dirs, files in os.walk(os.path.join(data_dir, o, x)):
                        if root.endswith('func'):
                            for file in files:
                                if file.endswith(".nii.gz"):
                                    split = file.split('_')
                                    subject = split[0].split('-')[1]
                                    session = split[1].split('-')[1]
                                    acquisition = split[2].split('-')[1]
                                    type = split[3].split('.')[0]
                                    uid = file.split('.')[0]
                                    data_selection = pd.concat([data_selection, pd.DataFrame(
                                        [[data_set, subject, session, acquisition, type, uid]],
                                        columns=['data_set', 'subject', 'session', 'acquisition', 'type', 'uid',
                                                 'path'])])

    return data_selection


dataselection_anat = make_dataselection_anat(data_dir=data_dir, studies=studies)
dataselection_func = make_dataselection_anat(data_dir=data_dir, studies=studies)
data_selection = dataselection_anat.append(dataselection_func)
data_selection.to_csv('../data/data_selection.csv')
