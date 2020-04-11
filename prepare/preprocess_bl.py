from samri.pipelines.preprocess import generic
from samri.pipelines import manipulations
from subjects_reader import find_subjects

scratch_dir = '~/.scratch/mlebe'
subjects = find_subjects()
bids_base = '{}/bids'.format(scratch_dir)

# Preprocess all of the data:
generic(bids_base,
	'/usr/share/mouse-brain-atlases/dsurqec_200micron.nii',
	registration_mask='/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
	functional_match={'acquisition':['EPI'],},
	structural_match={'acquisition':['TurboRARE'],},
	out_base='{}/preprocessing'.format(scratch_dir),
	workflow_name='generic_masked',
	model_prediction_mask = True,
	keep_work= True,
	subjects= subjects,
		)

generic(bids_base,
	'/usr/share/mouse-brain-atlases/dsurqec_200micron.nii',
	registration_mask='/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
	functional_match={'acquisition':['EPI'],},
	structural_match={'acquisition':['TurboRARE'],},
	out_base='{}/preprocessing'.format(scratch_dir),
	workflow_name='generic',
	keep_work= True,
	subjects= subjects,
		)