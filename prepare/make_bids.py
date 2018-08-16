from samri.pipelines.reposit import bru2bids

data_dir = '~/ni_data/ofM.dr'

bru2bids(data_dir,
	inflated_size=False,
	functional_match={"acquisition":["EPIlowcov"]},
	structural_match={"acquisition":["TurboRARElowcov"]},
	)
