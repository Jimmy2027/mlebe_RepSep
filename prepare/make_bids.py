import numpy as np
import pandas as pd
import os
from samri.pipelines.reposit import bru2bids
from labbookdb.report.selection import animal_id, parameterized
from datetime import datetime

db_path = '~/syncdata/meta.db'
data_dir = '/usr/share/irsabi_data/'
scratch_dir = os.path.expanduser('~/.scratch')
base_dir = '{}/irsabi'.format(scratch_dir)
bru2bids(data_dir,
	inflated_size=False,
	functional_match={
		'acquisition':['EPIlowcov'],
		},
	structural_match={
		'acquisition':['TurboRARElowcov'],
		},
	keep_crashdump=True,
	out_base=base_dir,
	)

# Add irregularity metadata
subjects_ldb = [i[4:] for i in os.listdir('{}/irsabi/bids'.format(scratch_dir)) if i.startswith('sub')]
subjects = [animal_id(db_path, 'ETH/AIC', i) for i in subjects_ldb]

subjects_info = parameterized(db_path, 'animals info', animal_filter=subjects)
convert_column_names = {
	'AnimalExternalIdentifier_identifier':'subject',
	'Animal_birth_date': 'birth_date',
	'Animal_sex': 'sex',
	}
subjects_info = subjects_info.loc[subjects_info['AnimalExternalIdentifier_database']=='ETH/AIC', convert_column_names.keys()]
subjects_info = subjects_info.rename(columns=convert_column_names)
subjects_info['age [d]'] = ''

irregularities = parameterized(db_path,'animals measurements irregularities',animal_filter=subjects)

bids_dir = '{}/bids'.format(base_dir)
for sub_dir in os.listdir(bids_dir):
	sub_path = os.path.join(bids_dir,sub_dir)
	if os.path.isdir(sub_path) and sub_dir[:4] == 'sub-':
		sessions_file = os.path.join(sub_path,'{}_sessions.tsv'.format(sub_dir))
		if os.path.isfile(sessions_file):
			sessions = pd.read_csv(sessions_file, sep='\t')
			sessions['irregularities']=''
			first_session_date = sessions['acq_time'].min()
			first_session_date = datetime.strptime(first_session_date,'%Y-%m-%dT%H:%M:%S')
			age = first_session_date - subjects_info.loc[subjects_info['subject']==sub_dir[4:],'birth_date']
			age = age/np.timedelta64(1, 'D')
			age = np.round(age)
			subjects_info.loc[subjects_info['subject']==sub_dir[4:],'age [d]'] = age
			for mydate in sessions['acq_time'].unique():
				mydate_date = datetime.strptime(mydate,'%Y-%m-%dT%H:%M:%S')
				irregularity_list = irregularities.loc[irregularities['Measurement_date']==mydate_date,'Irregularity_description'].tolist()
				irregularity_list = '; '.join(irregularity_list)
				sessions.loc[sessions['acq_time']==mydate,'irregularities'] = irregularity_list
			sessions.to_csv(sessions_file, sep='\t', index=False)

subjects_info = subjects_info.drop('birth_date', 1)
subjects_info.to_csv('{}/participants.tsv'.format(bids_dir), sep='\t', index=False)
subjects_info.to_csv('../data/participants.tsv'.format(bids_dir), sep='\t', index=False)
