from os import path
from samri.pipelines import glm

preprocess_base = '~/ni_data/ofM.dr/l1/'

masks = {
	'generic':'/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
	'generic_ambmc':'/usr/share/mouse-brain-atlases/ambmc_200micron_mask.nii',
	'legacy':'/usr/share/mouse-brain-atlases/lambmc_200micron_mask.nii',
	'legacy_dsurqec':'/usr/share/mouse-brain-atlases/ldsurqec_200micron_mask.nii',
	}

for key in masks:
	#We filter by run, since the primary contrast is replaced by the statistic contrast in level2
	glm.l2_common_effect(path.join(preprocess_base,key),
		workflow_name=key,
		mask=masks[key],
		keep_work=False,
		n_jobs_percentage=.33,
		match={'run':['1']},
		out_base='~/ni_data/ofM.dr/l2'
		)
	glm.l2_common_effect(path.join(preprocess_base,key),
		workflow_name=key,
		mask=masks[key],
		keep_work=False,
		n_jobs_percentage=.33,
		match={'run':['0']},
		out_base='~/ni_data/ofM.dr/l2'
		)
