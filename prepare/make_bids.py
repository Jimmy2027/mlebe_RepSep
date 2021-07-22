import os
from datetime import datetime

import numpy as np
import pandas as pd
from mlebe.training.utils.utils import json_file_to_pyobj
from samri.pipelines.reposit import bru2bids

from make_config import CONFIG_PATH as config_path, SCRATCH_DIR as scratch_dir


def produce_bids():
    from labbookdb.report.selection import animal_id, parameterized
    db_path = '~/syncdata/meta.db'
    data_dir = '/usr/share/drlfom_data/'

    scratch_dir = os.path.expanduser('~/.scratch')
    base_dir = '{}/mlebe'.format(scratch_dir)
    bru2bids(data_dir,
             inflated_size=False,
             functional_match={
                 'acquisition': ['EPIlowcov'],
             },
             structural_match={
                 'acquisition': ['TurboRARElowcov'],
             },
             keep_crashdump=True,
             out_base=base_dir,
             )

    # Add irregularity metadata
    subjects_ldb = [i[4:] for i in os.listdir('{}/mlebe/bids'.format(scratch_dir)) if i.startswith('sub')]
    subjects = [animal_id(db_path, 'ETH/AIC', i) for i in subjects_ldb]

    subjects_info = parameterized(db_path, 'animals info', animal_filter=subjects)
    convert_column_names = {
        'AnimalExternalIdentifier_identifier': 'subject',
        'Animal_birth_date': 'birth_date',
        'Animal_sex': 'sex',
    }
    subjects_info = subjects_info.loc[
        subjects_info['AnimalExternalIdentifier_database'] == 'ETH/AIC', convert_column_names.keys()]
    subjects_info = subjects_info.rename(columns=convert_column_names)
    subjects_info['age [d]'] = ''

    irregularities = parameterized(db_path, 'animals measurements irregularities', animal_filter=subjects)

    bids_dir = '{}/bids'.format(base_dir)
    for sub_dir in os.listdir(bids_dir):
        sub_path = os.path.join(bids_dir, sub_dir)
        if os.path.isdir(sub_path) and sub_dir[:4] == 'sub-':
            sessions_file = os.path.join(sub_path, '{}_sessions.tsv'.format(sub_dir))
            if os.path.isfile(sessions_file):
                sessions = pd.read_csv(sessions_file, sep='\t')
                sessions['irregularities'] = ''
                first_session_date = sessions['acq_time'].min()
                first_session_date = datetime.strptime(first_session_date, '%Y-%m-%dT%H:%M:%S')
                age = first_session_date - subjects_info.loc[subjects_info['subject'] == sub_dir[4:], 'birth_date']
                age = age / np.timedelta64(1, 'D')
                age = np.round(age)
                subjects_info.loc[subjects_info['subject'] == sub_dir[4:], 'age [d]'] = age
                for mydate in sessions['acq_time'].unique():
                    mydate_date = datetime.strptime(mydate, '%Y-%m-%dT%H:%M:%S')
                    irregularity_list = irregularities.loc[
                        irregularities['Measurement_date'] == mydate_date, 'Irregularity_description'].tolist()
                    irregularity_list = '; '.join(irregularity_list)
                    sessions.loc[sessions['acq_time'] == mydate, 'irregularities'] = irregularity_list
                sessions.to_csv(sessions_file, sep='\t', index=False)

    subjects_info = subjects_info.drop('birth_date', 1)
    subjects_info.to_csv('{}/participants.tsv'.format(bids_dir), sep='\t', index=False)
    subjects_info.to_csv('../data/participants.tsv'.format(bids_dir), sep='\t', index=False)


if __name__ == '__main__':
    config = json_file_to_pyobj(config_path)

    if not os.path.exists(os.path.expanduser(os.path.join(scratch_dir, 'bids'))):
        if os.path.exists('/usr/share/irsabi_bidsdata'):
            os.mkdir(os.path.expanduser(os.path.join(scratch_dir, 'bids')))
            if config.workflow_config.subjects:
                subjects = config.workflow_config.subjects
                for subject in subjects:
                    command = f'ln -s /usr/share/irsabi_bidsdata/sub-{subject} ~/.scratch/mlebe/bids/'
                    os.system(command)
                command = 'cp /usr/share/irsabi_bidsdata/dataset_description.json ~/.scratch/mlebe/bids/'
                os.system(command)
            else:
                command = 'ln -s /usr/share/irsabi_bidsdata/* ~/.scratch/mlebe/bids/'
                os.system(command)
        else:
            print("No IRSABI BIDS data distribution found, processing from scanner IRSABI data:")
            produce_bids()

    if config.workflow_config.with_FLASH:
        if not os.path.exists(os.path.expanduser(os.path.join(scratch_dir, 'dargcc_bids'))):
            if os.path.exists('/usr/share/dargcc_bidsdata'):
                os.mkdir(os.path.expanduser(os.path.join(scratch_dir, 'dargcc_bids')))
                command = 'ln -s /usr/share/dargcc_bidsdata/* ~/.scratch/mlebe/dargcc_bids/'
                os.system(command)
            else:
                print("No DARGCC BIDS data distribution found, processing from scanner IRSABI data:")
