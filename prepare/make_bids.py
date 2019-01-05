from samri.pipelines.reposit import bru2bids

scratch_dir = '~/data_scratch/irsabi'

bru2bids('/usr/share/irsabi',
	inflated_size=False,
	functional_match={"acquisition":["EPIlowcov"]},
	structural_match={"acquisition":["TurboRARElowcov"]},
	out_base=scratch_dir,
	)
