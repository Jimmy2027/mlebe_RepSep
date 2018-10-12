from nilearn.plotting import plot_anat
from samri.plotting.maps import scaled_plot
import matplotlib.pyplot as plt

template = '/usr/share/mouse-brain-atlases/dsurqec_40micron_masked.nii'

# we explicitly define a figure, because the one internally defined by nilearn overrides matplotlibrc
# https://github.com/nilearn/nilearn/issues/1777
fig = plt.figure()
scaled_plot(template,
        cut=(0,0,0,),
        threshold=1,
        cmap='gray',
        scale=0.2,
        dim=0.1,
        fig=fig,
        )
