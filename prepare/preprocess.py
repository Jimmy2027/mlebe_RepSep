from samri.pipelines.preprocess import generic, legacy
from samri.pipelines import manipulations

scratch_dir = '~/.scratch/irsabi'

bids_base = '{}/bids'.format(scratch_dir)

# Preprocess all of the data:
generic(bids_base,
	'/usr/share/mouse-brain-atlases/ambmc_200micron.nii',
	registration_mask='/usr/share/mouse-brain-atlases/ambmc_200micron_mask.nii',
	functional_match={'acquisition':['EPIlowcov'],},
	structural_match={'acquisition':['TurboRARElowcov'],},
	out_base='{}/preprocessing'.format(scratch_dir),
	workflow_name='generic_ambmc',
	)
legacy(bids_base,
	'/usr/share/mouse-brain-atlases/ldsurqec_200micron_masked.nii',
	functional_match={'acquisition':['EPIlowcov']},
	out_base='{}/preprocessing'.format(scratch_dir),
	workflow_name='legacy_dsurqec',
	n_jobs_percentage=0.6,
	)
generic(bids_base,
	'/usr/share/mouse-brain-atlases/dsurqec_200micron.nii',
	registration_mask='/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
	functional_match={'acquisition':['EPIlowcov'],},
	structural_match={'acquisition':['TurboRARElowcov'],},
	out_base='{}/preprocessing'.format(scratch_dir),
	workflow_name='generic',
	)
legacy(bids_base,
	'/usr/share/mouse-brain-atlases/lambmc_200micron.nii',
	functional_match={'acquisition':['EPIlowcov']},
	out_base='{}/preprocessing'.format(scratch_dir),
	workflow_name='legacy',
	n_jobs_percentage=0.6,
	)
