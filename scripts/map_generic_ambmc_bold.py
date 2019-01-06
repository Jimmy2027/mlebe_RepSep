import samri.plotting.maps as maps
from os import path

stat_map = '/home/chymera/ni_data/ofM.dr/l2/generic_ambmc/acq-EPIlowcov_run-0_tstat.nii.gz'
template = '/usr/share/mouse-brain-atlases/ambmc_40micron.nii'
maps.stat(stat_maps=[stat_map],
	template=template,
	#overlays=['/usr/share/mouse-brain-atlases/ambmc_200micron_roi-dr.nii'],
	#cut_coords=[(0.1,-0.8,0.6)],
	annotate=True,
	scale=0.2,
	show_plot=False,
	interpolation=None,
	draw_colorbar=True,
	black_bg=False,
	threshold=1,
	dim=0.2,
	)
