from os import path
from samri.pipelines import glm

preprocess_base = '~/ni_data/ofM.dr/preprocessing/'

masks = {
	'generic':'/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
	'generic_ambmc':'/usr/share/mouse-brain-atlases/ambmc_200micron_mask.nii.gz',
	'legacy':'/usr/share/mouse-brain-atlases/lambmc_200micron_mask.nii.gz',
	'legacy_dsurqec':"/usr/share/mouse-brain-atlases/ldsurqec_200micron_mask.nii.gz",
	}

for key in masks:
	glm.l1(path.join(preprocess_base,key),
		workflow_name=key,
		habituation="confound",
		mask=masks[key],
		keep_work=False,
		n_jobs_percentage=.33,
		match={'type':['cbv']},
		invert=True,
		out_base='~/ni_data/ofM.dr/l1'
		)
	glm.l1(path.join(preprocess_base,key),
		workflow_name=key,
		habituation="confound",
		mask=masks[key],
		keep_work=False,
		n_jobs_percentage=.33,
		match={'type':['bold']},
		invert=False,
		out_base='~/ni_data/ofM.dr/l1'
		)
