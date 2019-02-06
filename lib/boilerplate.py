import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from os import path
from lib.utils import float_to_tex, inline_anova, inline_factor

def fstatistic(factor,
	df_path='data/volumes.csv',
	dependent_variable='Volume Change Factor',
	expression='Processing*Template',
	exclusion_criteria={},
	**kwargs
	):
	df_path = path.abspath(df_path)
	df = pd.read_csv(df_path)

	df = df.loc[df['Processing']!='Unprocessed']

	for key in exclusion_criteria.keys():
		df = df.loc[~df[key].isin(exclusion_criteria[key])]

	formula='Q("{}") ~ {}'.format(dependent_variable, expression)
	ols = smf.ols(formula, df).fit()
	anova = sm.stats.anova_lm(ols, typ=2)
	tex = inline_anova(anova, factor, 'tex', **kwargs)
	return tex

def factorci(factor,
	df_path='data/volumes.csv',
	dependent_variable='Volume Change Factor',
	expression='Processing*Template',
	exclusion_criteria={},
	**kwargs
	):
	df_path = path.abspath(df_path)
	df = pd.read_csv(df_path)

	df = df.loc[df['Processing']!='Unprocessed']

	for key in exclusion_criteria.keys():
		df = df.loc[~df[key].isin(exclusion_criteria[key])]

	formula = 'Q("{}") ~ {}'.format(dependent_variable, expression)
	model = smf.mixedlm(formula, df, groups='Uid')
	fit = model.fit()
	summary = fit.summary()
	tex = inline_factor(summary, factor, 'tex', **kwargs)
	return tex

def corecomparison_factorci(factor,
	df_path='data/volumes.csv',
	dependent_variable='Volume Change Factor',
	expression='Processing*Contrast',
	exclusion_criteria={},
	**kwargs
	):
	df_path = path.abspath(df_path)
	df = pd.read_csv(df_path)

	df = df.loc[df['Processing']!='Unprocessed']
	df = df.loc[((df['Processing']=='Legacy') & (df['Template']=='Legacy')) | ((df['Processing']=='Generic') & (df['Template']=='Generic'))]

	for key in exclusion_criteria.keys():
		df = df.loc[~df[key].isin(exclusion_criteria[key])]

	formula = 'Q("{}") ~ {}'.format(dependent_variable, expression)
	model = smf.mixedlm(formula, df, groups='Uid')
	fit = model.fit()
	summary = fit.summary()
	#print(summary)
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
	dependent_variable='Volume Change Factor',
	max_len=2,
	**kwargs
	):

	df_path = path.abspath(df_path)
	df = pd.read_csv(df_path)

	df = df.loc[df['Processing']!='Unprocessed']

	if template:
		df = df.loc[df['Template']==template]
	legacy = np.var(df.loc[df['Processing']=='Legacy', dependent_variable].tolist())
	generic = np.var(df.loc[df['Processing']=='Generic', dependent_variable].tolist())


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

def variance_test(
        factor,
        workflow,
        metric,
        df_path='data/variance_data.csv',
        template=False,
        max_len=2,
        **kwargs
        ):
        df = pd.read_csv(path.abspath(df_path))
        df = df.loc[df['Processing']==workflow]
        #contrast
        df = df.loc[df['acquisition'].str.contains('cbv')]
        model= metric + '~ C(Subject) + C(Session)'
        ols = smf.ols(model, df).fit()
        anova = sm.stats.anova_lm(ols, typ=3, robust='hc3')
        tex = inline_anova(anova,  factor, 'tex', **kwargs)
        return tex

def fstatistic_smoothness(factor,
        df_path='data/smoothness_data.csv',
        dependent_variable='Smoothness Change Factor',
        expression='Processing*Template',
        exclusion_criteria={},
        **kwargs
        ):
        df_path = path.abspath(df_path)
        df = pd.read_csv(df_path)

        df = df.loc[df['Processing']!='Unprocessed']

        for key in exclusion_criteria.keys():
                df = df.loc[~df[key].isin(exclusion_criteria[key])]

        formula='Q("{}") ~ {}'.format(dependent_variable, expression)
        ols = smf.ols(formula, df).fit()
        anova = sm.stats.anova_lm(ols, typ=2)
        tex = inline_anova(anova, factor, 'tex', **kwargs)
        return tex

def meanVar(ret,
        df_path='data/smoothness_data.csv',
        factor = 'Smoothness Change Factor',
        Processing = 'Legacy',
        template=False,
        max_len=2,
        **kwargs
        ):
        df_path = path.abspath(df_path)
        df = pd.read_csv(df_path)

        df = df.loc[df['Processing']!='Unprocessed']
        data = df.loc[df['Processing']==Processing, factor]

        if(ret == 'mean'):
                result = data.mean()
        if(ret == 'sd'):
                result = data.std()

        return float_to_tex(result, max_len, **kwargs)

