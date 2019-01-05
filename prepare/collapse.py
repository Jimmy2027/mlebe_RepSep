from samri.pipelines.preprocess import generic, legacy
from samri.pipelines import manipulations

scratch_dir = '~/data_scratch/irsabi'

bids_base = '{}/bids'.format(scratch_dir)

# Create 3D collapsed dataset to speed up repeated evaluations
# Uncomment n_jobs_percentage parameter for machines with limited memory,
# or comment them out for machines with plenty of memory.
manipulations.collapse_nifti(bids_base,
	'{}/bids_collapsed'.format(scratch_dir),
	n_jobs_percentage=0.66,
	)
manipulations.collapse_nifti('{}/preprocessing/generic_ambmc'.format(scratch_dir),
	'{}/preprocessing/generic_ambmc_collapsed'.format(scratch_dir),
	n_jobs_percentage=0.33,
	)
manipulations.collapse_nifti('{}/preprocessing/legacy_dsurqec'.format(scratch_dir),
	'{}/preprocessing/legacy_dsurqec_collapsed'.format(scratch_dir),
	n_jobs_percentage=0.33,
	)
manipulations.collapse_nifti('{}/preprocessing/generic'.format(scratch_dir),
	'{}/preprocessing/generic_collapsed'.format(scratch_dir),
	n_jobs_percentage=0.33,
	)
manipulations.collapse_nifti('{}/preprocessing/legacy'.format(scratch_dir),
	'{}/preprocessing/legacy_collapsed'.format(scratch_dir),
	n_jobs_percentage=0.33,
	)
