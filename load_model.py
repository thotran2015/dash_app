import pickle 

from lifelines import CoxPHFitter 
import pandas as pd
import numpy as np

def get_patient_profiles(file):
 	data = pd.read_csv(file).rename(columns ={'Unnamed: 0': 'Patient'})
 	data = data.set_index('Patient')
 	return data

def fit_lifelines_model(data):
 	cph = CoxPHFitter()
 	model = cph.fit(data, duration_col= 'age_censor', event_col='breastcancer')
 	return model 

def get_covariate_groups(model, covariate, val_range):
    axes2 = model.plot_covariate_groups(covariate, values=val_range, cmap='coolwarm', label = 'covs', plot_baseline=False)
    lines = axes2.get_lines()
    axes2.clear()
    return {i.get_label(): i.get_data() for i in lines}

    

def get_partial_hazard_ratio(model):
    cov_grps = model.summary.index
    lower = model.summary['exp(coef) lower 95%']
    upper = model.summary['exp(coef) upper 95%']
    target = model.summary['exp(coef)']
    df = pd.DataFrame([lower, target, upper])
    return {col: list(df[col].values) for col in df.columns}


def load_model(model_loc):
    with open(model_loc, "rb") as input_file:
        model = pickle.load(input_file) 
        print(model.summary.index)
        print(model.summary.columns)
        return model

#with open("BRCA2_model.pickle", "rb") as input_file:
    # model = pickle.load(input_file) 
    # print(model.summary.columns)
    # lower = np.exp(model.summary['lower 0.95'])
    # upper = np.exp(model.summary['upper 0.95'])
    # target = model.summary['exp(coef)']
    # df = pd.DataFrame([lower, target, upper])
    # print(get_partial_hazard_ratio(model))
    #print(get_partial_hazard_ratio(model)['log Allele Frequency'].values)
    #print(df.T.plot())
    #model.plot(hazard_ratios = True, label = "hello")
    #model.plot_covariate_groups(covariate, values=val_range, cmap='coolwarm')
    
    
    
#  axes1 = model.plot(hazard_ratios = True, label = 'HR')
#  #plt = model.plot(hazard_ratios = True)
# # print({l: p.get_data() for l, p in axes1.items()})
#  #cov_grps = model.summary.index
#  lines = axes1.get_lines()
 
#  #print(np.exp(model.summary['lower 0.95']))
#  #print(np.exp(model.summary['upper 0.95']))
#  vlines = pd.DataFrame([e.get_data()[0] for e in lines], columns = cov_grps)
#  axes1.clear()
#  vlines['data_labels'] = ['target', 'lower_bound', 'upper_bound']
 
#  vlines = vlines.set_index('data_labels')
#  print(vlines)