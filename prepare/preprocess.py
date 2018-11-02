from samri.pipelines.preprocess import generic, legacy
from samri.pipelines import manipulations

bids_base = '~/ni_data/ofM.dr/bids'

# Preprocess all of the data:
generic(bids_base, "~/ambmc_200micron.nii.gz",
	registration_mask="~/ambmc_200micron_mask.nii.gz",
	functional_match={'acquisition':['EPIlowcov'],},
	structural_match={'acquisition':['TurboRARElowcov'],},
	actual_size=True,
	out_base='~/ni_data/ofM.dr/preprocessing',
	workflow_name='generic_ambmc',
	)
legacy(bids_base, '~/ldsurqec_200micron_masked.nii.gz',
	functional_match={'acquisition':['EPIlowcov']},
	out_base='~/ni_data/ofM.dr/preprocessing',
	workflow_name='legacy_dsurqec',
	)
generic(bids_base, "/usr/share/mouse-brain-atlases/dsurqec_200micron.nii",
	registration_mask="/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii",
	functional_match={'acquisition':['EPIlowcov'],},
	structural_match={'acquisition':['TurboRARElowcov'],},
	actual_size=True,
	out_base='~/ni_data/ofM.dr/preprocessing',
	workflow_name='generic',
	)
legacy(bids_base, "/usr/share/mouse-brain-atlases/lambmc_200micron.nii",
	functional_match={'acquisition':['EPIlowcov']},
	out_base='~/ni_data/ofM.dr/preprocessing',
	workflow_name='legacy',
	)

# Create 3D collapsed dataset to speed up repeated evaluations
# Uncomment n_jobs_percentage parameter for machines with limited memory.
manipulations.collapse_nifti(bids_base,
	'~/ni_data/ofM.dr/bids_collapsed',
	#n_jobs_percentage=0.66,
	)
manipulations.collapse_nifti('~/ni_data/ofM.dr/preprocessing/generic_ambmc',
	'~/ni_data/ofM.dr/preprocessing/generic_ambmc_collapsed',
	#n_jobs_percentage=0.5,
	)
manipulations.collapse_nifti('~/ni_data/ofM.dr/preprocessing/legacy_dsurqec',
	'~/ni_data/ofM.dr/preprocessing/legacy_dsurqec_collapsed',
	#n_jobs_percentage=0.5,
	)
manipulations.collapse_nifti('~/ni_data/ofM.dr/preprocessing/generic',
	'~/ni_data/ofM.dr/preprocessing/generic_collapsed',
	#n_jobs_percentage=0.5,
	)
manipulations.collapse_nifti('~/ni_data/ofM.dr/preprocessing/legacy',
	'~/ni_data/ofM.dr/preprocessing/legacy_collapsed',
	#n_jobs_percentage=0.5,
	)
