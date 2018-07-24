bids_base = '~/ni_data/ofM.dr/bids'
generic(bids_base, "/usr/share/mouse-brain-atlases/dsurqec_200micron.nii",
	registration_mask="/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii",
	functional_match={'type':['cbv'],},
	structural_match={'acquisition':['TurboRARElowcov'],},
	actual_size=True,
	functional_registration_method="composite",
	negative_contrast_agent=True,
	out_base='~/ni_data/ofM.dr/preprocessing',
	keep_work=True,
	)
generic(bids_base, "/usr/share/mouse-brain-atlases/dsurqec_200micron.nii",
	registration_mask="/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii",
	functional_match={'type':['bold'],},
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

