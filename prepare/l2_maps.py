from os import path
from samri.pipelines import glm

scratch_dir = '~/data_scratch/irsabi'

preprocess_base = '{}/l1/'.format(scratch_dir)

masks = {
	'generic':'/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
	'generic_ambmc':'/usr/share/mouse-brain-atlases/ambmc_200micron_mask.nii',
	'legacy':'/usr/share/mouse-brain-atlases/lambmc_200micron_mask.nii',
	'legacy_dsurqec':'/usr/share/mouse-brain-atlases/ldsurqec_200micron_mask.nii',
	}

for key in masks:
	#We filter by run, since the primary contrast is replaced by the statistic contrast in level2.
	#We exclude animal 4006, as its slice positioning significantly diminishes statistic coverage.
	glm.l2_common_effect(path.join(preprocess_base,key),
		workflow_name=key,
		mask=masks[key],
		groupby='none',
		keep_work=False,
		n_jobs_percentage=.33,
		exclude={'subject':['4006'],},
		include={'run':['0'],},
		out_base='{}/l2'.format(scratch_dir),
		)
	glm.l2_common_effect(path.join(preprocess_base,key),
		workflow_name=key,
		mask=masks[key],
		groupby='none',
		keep_work=False,
		n_jobs_percentage=.33,
		exclude={'subject':['4006'],},
		include={'run':['1'],},
		out_base='{}/l2'.format(scratch_dir),
		)
