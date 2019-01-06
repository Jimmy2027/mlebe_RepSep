import samri.plotting.maps as maps
from os import path

stat_map = '/home/chymera/ni_data/ofM.dr/l2/legacy_dsurqec/acq-EPIlowcov_run-1_tstat.nii.gz'
template = '/usr/share/mouse-brain-atlases/ldsurqec_40micron_masked.nii'
maps.stat(stat_maps=[stat_map],
	template=template,
	#overlays=['/usr/share/mouse-brain-atlases/ldsurqec_200micron_roi-dr.nii'],
	#cut_coords=[(0,35,2)],
	annotate=True,
	scale=0.2,
	show_plot=False,
	interpolation=None,
	draw_colorbar=True,
	black_bg=False,
	threshold=1,
	dim=0.2,
	)
