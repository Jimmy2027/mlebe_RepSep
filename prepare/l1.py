from os import path
from samri.pipelines import glm

scratch_dir = '~/.scratch/mlebe'

preprocess_base = '{}/preprocessing/'.format(scratch_dir)

masks = {
	'generic':'/usr/share/mouse-brain-atlases/dsurqec_200micron_mask.nii',
	'generic_ambmc':'/usr/share/mouse-brain-atlases/ambmc_200micron_mask.nii',
	'legacy':'/usr/share/mouse-brain-atlases/lambmc_200micron_mask.nii',
	'legacy_dsurqec':'/usr/share/mouse-brain-atlases/ldsurqec_200micron_mask.nii',
	}

for key in masks:
	glm.l1(path.join(preprocess_base,key),
		bf_path='../data/chr_beta1.txt',
		workflow_name=key,
		habituation="confound",
		mask=masks[key],
		keep_work=False,
		n_jobs_percentage=.33,
		match={'type':['cbv']},
		invert=True,
		out_base='{}/l1'.format(scratch_dir)
		)
	glm.l1(path.join(preprocess_base,key),
		bf_path='../data/chr_beta1.txt',
		workflow_name=key,
		habituation="confound",
		mask=masks[key],
		keep_work=False,
		n_jobs_percentage=.33,
		match={'type':['bold']},
		invert=False,
		out_base='{}/l1'.format(scratch_dir)
		)
