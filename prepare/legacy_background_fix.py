# Legacy fixes required for statistical analysis of function:

import multiprocessing as mp
import os
from joblib import Parallel, delayed
from samri.pipelines.extra_functions import reset_background

legacy = os.walk(os.path.expanduser('~/ni_data/ofM.dr/preprocessing/legacy'))
legacy_dsurqec = os.walk(os.path.expanduser('~/ni_data/ofM.dr/preprocessing/legacy_dsurqec'))
in_files = []
for r,_,fs in list(legacy)+list(legacy_dsurqec):
	for f in fs:
		if f.endswith('.nii.gz'):
			in_files.append(os.path.join(r,f))

n_jobs = max(int(round(mp.cpu_count()*0.85)),2)
iter_length = len(in_files)
iter_data = Parallel(n_jobs=n_jobs, verbose=0, backend="threading")(map(delayed(reset_background),
                in_files,
                [0]*iter_length,
                in_files,
                [20]*iter_length,
                ))

