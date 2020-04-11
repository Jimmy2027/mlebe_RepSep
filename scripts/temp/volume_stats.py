import pandas as pd
import statsmodels.formula.api as smf
from lib.categorical import violinplot
from matplotlib import pyplot as plt
import matplotlib as mpl

bootstrapped_RMSEs = pd.read_csv('data/bootstrapped_volume.csv')

ax = violinplot(
	x='Contrast',
	y='RMSE',
	data=bootstrapped_RMSEs,
	hue="Processing",
	saturation=1,
	split=True,
	inner='quartile',
	palette='muted',
	scale='area',
	dodge=False,
	inner_linewidth=1.0,
	linewidth=mpl.rcParams['grid.linewidth'],
	linecolor='w',
	)

plt.savefig('test')

print(bootstrapped_RMSEs.loc[(bootstrapped_RMSEs['Processing'] == 'Generic Masked')].describe())
print(bootstrapped_RMSEs.loc[(bootstrapped_RMSEs['Processing'] == 'Generic')].describe())
dependent_variable = 'RMSE'
expression = 'Processing*Contrast'
formula = 'Q("{}") ~ {}'.format(dependent_variable, expression)
model = smf.mixedlm(formula, bootstrapped_RMSEs, groups='Uid')
fit = model.fit()
summary = fit.summary()
print(summary)