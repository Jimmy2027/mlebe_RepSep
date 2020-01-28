import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from os import path
from lib.utils import float_to_tex, inline_anova, inline_factor

def fstatistic(factor,
	df_path='data/volume.csv',
	dependent_variable='Volume Conservation Factor',
	# expression='Processing*Template',
	expression='Processing',
	exclusion_criteria={},
	**kwargs
	):
	df_path = path.abspath(df_path)
	df = pd.read_csv(df_path)

	df = df.loc[df['Processing']!='Unprocessed']

	for key in exclusion_criteria.keys():
		df = df.loc[~df[key].isin(exclusion_criteria[key])]
	# print(df)
	formula='Q("{}") ~ {}'.format(dependent_variable, expression)

	ols = smf.ols(formula, df).fit()
	
	anova = sm.stats.anova_lm(ols, typ=3)
	tex = inline_anova(anova, factor, 'tex', **kwargs)
	return tex

def factorci(factor,
	df_path='data/volume.csv',
	dependent_variable='Volume Conservation Factor',
	# expression='Processing*Template',
	expression='Processing',
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
	df_path='data/volume.csv',
	dependent_variable='Volume Conservation Factor',
	expression='Processing*Contrast',
	exclusion_criteria={},
	**kwargs
	):

	df_path = path.abspath(df_path)
	df = pd.read_csv(df_path)

	df = df.loc[df['Processing']!='Unprocessed']
	df = df.loc[((df['Processing']=='Generic Masked')) | ((df['Processing']=='Generic'))]

	for key in exclusion_criteria.keys():
		df = df.loc[~df[key].isin(exclusion_criteria[key])]

	formula = 'Q("{}") ~ {}'.format(dependent_variable, expression)
	model = smf.mixedlm(formula, df, groups='Uid')
	fit = model.fit()
	summary = fit.summary()
	tex = inline_factor(summary, factor, 'tex', **kwargs)
	return tex

def varianceratio(
	df_path='data/volume.csv',
	dependent_variable='Volume Conservation Factor',
	max_len=2,
	**kwargs
	):

	df_path = path.abspath(df_path)
	df = pd.read_csv(df_path)

	df = df.loc[df['Processing']!='Unprocessed']

	generic_masked = np.var(df.loc[df['Processing']=='Generic Masked', dependent_variable].tolist())
	generic = np.var(df.loc[df['Processing']=='Generic', dependent_variable].tolist())


	ratio = generic_masked/generic

	return float_to_tex(ratio, max_len, **kwargs)

def variance_test(
        factor,
        workflow,
        metric,
        df_path='data/variance.csv',
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

def print_dice():
	textfile = open('mlebe_figs/dice_score.txt', 'r')
	dice_score = textfile.readline()
	return np.round(float(dice_score), 3)

def print_testcorr_ytrue():
	corr_df = pd.read_csv('data/classifier/test_correlation_dataframe.csv')
	# corr = corr_df.loc[['x_test'], ['y_test']]
	return np.round(corr_df.values[1][1], 3)

def print_testcorr_ypred():
	corr_df = pd.read_csv('data/classifier/test_correlation_dataframe.csv')
	# corr = corr_df.loc[['x_test'], ['y_pred']]
	return np.round(corr_df.values[2][1], 3)

def print_blcorr_ytrue():
	corr_df = pd.read_csv('data/classifier/bl_correlation_dataframe.csv', index_col = 0)
	corr = corr_df.loc[['x_bl'], ['y_bl']]
	return np.round(corr.values[0][0], 3)

def print_blcorr_ypred():
	corr_df = pd.read_csv('data/classifier/bl_correlation_dataframe.csv', index_col = 0)
	corr = corr_df.loc[['x_bl'], ['y_pred']]
	return np.round(corr.values[0][0], 3)
