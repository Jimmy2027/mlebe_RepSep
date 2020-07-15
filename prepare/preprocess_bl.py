from samri.pipelines.preprocess import generic
from subjects_reader import find_subjects

scratch_dir = '~/.scratch/mlebe'
subjects = find_subjects()
bids_base = '{}/bids'.format(scratch_dir)
print(subjects)
# Preprocess all of the data:

generic(bids_base,
	'/usr/share/mouse-brain-atlases/dsurqec_200micron.nii',
	registration_mask='/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
	functional_match={'acquisition':['EPI'],},
	structural_match={'acquisition':['TurboRARE'],},
	out_base='{}/preprocessing'.format(scratch_dir),
	workflow_name='masked',
	keep_work= False,
	subjects= subjects,
		)