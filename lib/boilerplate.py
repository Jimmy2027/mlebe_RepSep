import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from os import path
from lib.utils import float_to_tex, inline_anova, inline_factor

def fstatistic(factor,
	df_path='data/volumes.csv',
	**kwargs
	):
	df_path = path.abspath(df_path)
	df = pd.read_csv(df_path)

	df = df.loc[df['Processing']!='Unprocessed']

	model='Q("Volume Change Factor") ~ Processing*Template'
	ols = smf.ols(model, df).fit()
	anova = sm.stats.anova_lm(ols, typ=2)
	tex = inline_anova(anova, factor, 'tex', **kwargs)
	return tex

def vc_factorci(factor,
	df_path='data/volumes.csv',
	**kwargs
	):
	df_path = path.abspath(df_path)
	df = pd.read_csv(df_path)

	df = df.loc[df['Processing']!='Unprocessed']

	model=smf.mixedlm('Q("Volume Change Factor") ~ Processing*Template', df, groups='Uid')
	fit = model.fit()
	summary = fit.summary()
	tex = inline_factor(summary, factor, 'tex', **kwargs)
	return tex

def vcc_factorci(factor,
	df_path='data/volumes.csv',
	**kwargs
	):
	df_path = path.abspath(df_path)
	df = pd.read_csv(df_path)

	df = df.loc[df['Processing']!='Unprocessed']
	df = df.loc[((df['Processing']=='Legacy') & (df['Template']=='Legacy')) | ((df['Processing']=='Generic') & (df['Template']=='Generic'))]

	model=smf.mixedlm('Q("Volume Change Factor") ~ Processing*Contrast', df, groups='Uid')

	fit = model.fit()
	summary = fit.summary()
	tex = inline_factor(summary, factor, 'tex', **kwargs)
	return tex

def varianceratio(
	df_path='data/volumes.csv',
	template=False,
	max_len=2,
	**kwargs
	):

	volume_path = path.abspath('data/volumes.csv')
	df = pd.read_csv(volume_path)

	df = df.loc[df['Processing']!='Unprocessed']

	if template:
		df = df.loc[df['Template']==template]
	legacy = np.var(df.loc[df['Processing']=='Legacy', 'Volume Change Factor'].tolist())
	generic = np.var(df.loc[df['Processing']=='Generic', 'Volume Change Factor'].tolist())


	ratio = legacy/generic

	return float_to_tex(ratio, max_len, **kwargs)
	# Hypothesis test, but we are not, in current cases, testing a hypothesis.
	#from scipy.stats import levene
	#result = levene(
	#	df.loc[df['Processing']=='Legacy', 'Volume Change Factor'].tolist(),
	#	df.loc[df['Processing']=='Generic', 'Volume Change Factor'].tolist(),
	#	)
	#print(float_to_tex(result.pvalue, max_len=3))

def variancep(
	df_path='data/volumes.csv',
	template=False,
	max_len=2,
	**kwargs
	):
	from scipy.stats import levene

	volume_path = path.abspath('data/volumes.csv')
	df = pd.read_csv(volume_path)

	df = df.loc[df['Processing']!='Unprocessed']

	if template:
		df = df.loc[df['Template']==template]
	result = levene(
		df.loc[df['Processing']=='Legacy', 'Volume Change Factor'].tolist(),
		df.loc[df['Processing']=='Generic', 'Volume Change Factor'].tolist(),
		)

	return float_to_tex(result.pvalue, max_len, **kwargs)
