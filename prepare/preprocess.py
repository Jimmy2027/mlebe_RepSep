from samri.pipelines.preprocess import generic, legacy
from samri.pipelines import manipulations

bids_base = '~/ni_data/ofM.dr/bids'

# Preprocess all of the data:
generic(bids_base,
	"/home/chymera/mouse-brain-atlas-0.1.20181111/ambmc_200micron.nii",
	registration_mask="/usr/share/mouse-brain-atlases/ambmc_200micron_mask.nii",
	functional_match={'acquisition':['EPIlowcov'],},
	structural_match={'acquisition':['TurboRARElowcov'],},
	actual_size=True,
	out_base='~/ni_data/ofM.dr/preprocessing',
	workflow_name='generic_ambmc',
	)
legacy(bids_base,
	'/usr/share/mouse-brain-atlases/ldsurqec_200micron_masked.nii',
	functional_match={'acquisition':['EPIlowcov']},
	out_base='~/ni_data/ofM.dr/preprocessing',
	workflow_name='legacy_dsurqec',
	)
generic(bids_base,
	"/usr/share/mouse-brain-atlases/dsurqec_200micron.nii",
	registration_mask="/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii",
	functional_match={'acquisition':['EPIlowcov'],},
	structural_match={'acquisition':['TurboRARElowcov'],},
	actual_size=True,
	out_base='~/ni_data/ofM.dr/preprocessing',
	workflow_name='generic',
	)
legacy(bids_base,
	"/usr/share/mouse-brain-atlases/lambmc_200micron.nii",
	functional_match={'acquisition':['EPIlowcov']},
	out_base='~/ni_data/ofM.dr/preprocessing',
	workflow_name='legacy',
	)
