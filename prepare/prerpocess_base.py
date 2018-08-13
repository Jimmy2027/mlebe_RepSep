from samri.pipelines.preprocess import generic, legacy
from samri.pipelines import manipulations

bids_base = '~/ni_data/ofM.dr/bids'

# Preprocess all of the data:
generic(bids_base, "/usr/share/mouse-brain-atlases/dsurqec_200micron.nii",
	registration_mask="/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii",
	functional_match={'acquisition':['EPIlowcov'],'type':['cbv'],},
	structural_match={'acquisition':['TurboRARElowcov'],},
	actual_size=True,
	functional_registration_method="composite",
	negative_contrast_agent=True,
	out_base='~/ni_data/ofM.dr/preprocessing',
	)
generic(bids_base, "/usr/share/mouse-brain-atlases/dsurqec_200micron.nii",
	registration_mask="/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii",
	functional_match={'acquisition':['EPIlowcov'],'type':['bold'],},
	structural_match={'acquisition':['TurboRARElowcov'],},
	actual_size=True,
	functional_registration_method="composite",
	out_base='~/ni_data/ofM.dr/preprocessing',
	)
legacy(bids_base, "/usr/share/mouse-brain-atlases/lambmc_200micron.nii",
	functional_match={'type':['cbv'],'acquisition':['EPIlowcov']},
	negative_contrast_agent=True,
	out_base='~/ni_data/ofM.dr/preprocessing',
	)
legacy(bids_base, "/usr/share/mouse-brain-atlases/lambmc_200micron.nii",
	functional_match={'type':['bold'],'acquisition':['EPIlowcov']},
	out_base='~/ni_data/ofM.dr/preprocessing',
	)

# Create 3D collapsed dataset to speed up repeated evaluations
manipulations.collapse_nifti('~/ni_data/ofM.dr/preprocessing/generic',
	'~/ni_data/ofM.dr/preprocessing/generic_collapsed',
	)
manipulations.collapse_nifti('~/ni_data/ofM.dr/preprocessing/legacy',
	'~/ni_data/ofM.dr/preprocessing/legacy_collapsed',
	)
