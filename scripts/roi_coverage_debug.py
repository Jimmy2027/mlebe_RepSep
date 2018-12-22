import samri.plotting.maps as maps
import os
import re

base_dir = '~/ni_data/ofM.dr/l1/generic/'
base_dir = os.path.abspath(os.path.expanduser(base_dir))
match_regex = 'sub-(?P<sub>[a-zA-Z0-9]+)_ses-(?P<ses>[a-zA-Z0-9]+)_.*?run-(?P<run>[0-9]+).*?_tstat.(?:nii|nii\.gz)'


stat_maps = []
names = []
print(base_dir)
for p,d,fs in os.walk(base_dir):
	if fs:
		for f in fs:
			m = re.match(match_regex, f)
			if m:
				stat_maps.append(p+'/'+f)
				names.append('/tmp/sub-{}_ses-{}_run-{}.png'.format(*m.groups()))

for stat_map, name in zip(stat_maps,names):
	template = '/usr/share/mouse-brain-atlases/dsurqec_40micron_masked.nii'
	maps.stat(stat_maps=[stat_map],
		template=template,
		overlays=['/usr/share/mouse-brain-atlases/dsurqec_200micron_roi-dr.nii'],
		cut_coords=[(0,-4.5,-2.9)],
		annotate=True,
		scale=0.2,
		show_plot=False,
		interpolation=None,
		draw_colorbar=True,
		black_bg=False,
		threshold=2,
		dim=0.2,
		save_as=name,
		)
