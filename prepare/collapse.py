from samri.pipelines.preprocess import generic, legacy
from samri.pipelines import manipulations

bids_base = '~/ni_data/ofM.dr/bids'

# Create 3D collapsed dataset to speed up repeated evaluations
# Uncomment n_jobs_percentage parameter for machines with limited memory,
# or comment them out for machines with plenty of memory.
manipulations.collapse_nifti(bids_base,
	'~/ni_data/ofM.dr/bids_collapsed',
	n_jobs_percentage=0.66,
	)
manipulations.collapse_nifti('~/ni_data/ofM.dr/preprocessing/generic_ambmc',
	'~/ni_data/ofM.dr/preprocessing/generic_ambmc_collapsed',
	n_jobs_percentage=0.5,
	)
manipulations.collapse_nifti('~/ni_data/ofM.dr/preprocessing/legacy_dsurqec',
	'~/ni_data/ofM.dr/preprocessing/legacy_dsurqec_collapsed',
	n_jobs_percentage=0.5,
	)
manipulations.collapse_nifti('~/ni_data/ofM.dr/preprocessing/generic',
	'~/ni_data/ofM.dr/preprocessing/generic_collapsed',
	n_jobs_percentage=0.5,
	)
manipulations.collapse_nifti('~/ni_data/ofM.dr/preprocessing/legacy',
	'~/ni_data/ofM.dr/preprocessing/legacy_collapsed',
	n_jobs_percentage=0.5,
	)
