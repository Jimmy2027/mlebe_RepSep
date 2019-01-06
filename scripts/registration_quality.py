import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from os import path
from samri.plotting.aggregate import registration_qc
from samri.typesetting import inline_anova
from samri.development import reg_cc
from samri.pipelines.reposit import bru2bids
from samri.pipelines.preprocess import full_prep, legacy_bruker
from samri.examples.registration_qc import evaluateMetrics
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np



# preprocess the data
# ------------------
bids_base = '~/ni_data/ofM.dr/bids/'
template = '/usr/share/mouse-brain-atlases/dsurqec_200micron.nii'

full_prep(bids_base,
	"mouse",
       # comma is important since otherwise tuple instead of dict
	functional_match={'acquisition':['EPIlowcov'],},
	structural_match={'acquisition':['TurboRARElowcov'],},
	actual_size=True,
	functional_registration_method="composite",
	negative_contrast_agent=True,
	keep_work=True,
	out_dir="preprocessing_ours"
	)

legacy_bruker(bids_base,
       "mouse",
       # comma is important since otherwise tuple instead of dict
       functional_match={'acquisition':['EPIlowcov'],},
       structural_match={'acquisition':['TurboRARElowcov'],},
       negative_contrast_agent=True,
       keep_work=True,
       out_dir="preprocessing_legacy"
       )

reg_cc(path=bids_base + "preprocessing_ours/generic/", save = "./f_reg_quality_ours", template=template, autofind=True)
reg_cc(path=bids_base + "preprocessing_legacy/generic/", save = "./f_reg_quality_legacy", template=template, autofind=True)

metrics_ours, means_ours, stds_ours = evaluateMetrics(fname="./f_reg_quality_ours", metrics=['CC', 'GC'])
metrics_legacy, means_legacy, stds_legacy = evaluateMetrics(fname="./f_reg_quality_legacy")

plotting = pd.DataFrame(np.vstack((stds_ours, stds_legacy)), columns = ['ours', 'legacy'])
plotting = plotting.set_index(np.asarray(metrics).transpose())
ax = plotting.plot(kind='bar', use_index=True, rot=90)
ax.set_xlabel('Metric')
ax.set_ylabel('Variance')
fig = ax.get_figure()
fig.savefig('VarianceOverMetric.png')
