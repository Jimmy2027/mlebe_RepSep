import samri.plotting.maps as maps
from os import path

stat_map = '~/data_scratch/irsabi/l2/generic_ambmc/acq-EPIlowcov_run-0_tstat.nii.gz'
template = '/usr/share/mouse-brain-atlases/ambmc_40micron.nii'
maps.stat(stat_maps=[stat_map],
	template=template,
	overlays=['data/acquisition_area_ambmc.nii.gz'],
	annotate=True,
	scale=0.2,
	show_plot=False,
	interpolation=None,
	draw_colorbar=True,
	black_bg=False,
	threshold=1,
	dim=0.2,
	)
