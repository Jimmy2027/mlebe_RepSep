from samri.pipelines.preprocess import generic, legacy
from samri.pipelines import manipulations

bids_base = '~/ni_data/ofM.dr/bids'

# Preprocess all of the data:
generic(bids_base, "/usr/share/mouse-brain-atlases/dsurqec_200micron.nii",
	registration_mask="/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii",
	functional_match={'acquisition':['EPIlowcov'],},
	structural_match={'acquisition':['TurboRARElowcov'],},
	actual_size=True,
	out_base='~/ni_data/ofM.dr/preprocessing',
	)
legacy(bids_base, "/usr/share/mouse-brain-atlases/lambmc_200micron.nii",
	functional_match={'acquisition':['EPIlowcov']},
	out_base='~/ni_data/ofM.dr/preprocessing',
	)

# Create 3D collapsed dataset to speed up repeated evaluations
manipulations.collapse_nifti(bids_base,
	'~/ni_data/ofM.dr/bids_collapsed',
	)
manipulations.collapse_nifti('~/ni_data/ofM.dr/preprocessing/generic',
	'~/ni_data/ofM.dr/preprocessing/generic_collapsed',
	)
manipulations.collapse_nifti('~/ni_data/ofM.dr/preprocessing/legacy',
	'~/ni_data/ofM.dr/preprocessing/legacy_collapsed',
	)
