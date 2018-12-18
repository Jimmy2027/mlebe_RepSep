import samri.plotting.maps as maps
from os import path

stat_map = '/home/chymera/ni_data/ofM.dr/l2/generic_ambmc/ses-ofM/acq-EPIlowcov_run-1_tstat.nii.gz'
template = '/usr/share/mouse-brain-atlases/ambmc_40micron.nii'
maps.stat(stat_maps=[stat_map],
        template=template,
        cut_coords=[(0,-4.5,-2.9)],
        annotate=True,
        scale=0.5,
        show_plot=False,
        interpolation=None,
        draw_colorbar=True,
        black_bg=False,
        threshold=3,
        dim=0.2,
        )
