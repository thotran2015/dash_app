import pickle 

from lifelines import CoxPHFitter 
import pandas as pd

def get_patient_profiles(file):
 	data = pd.read_csv(file).rename(columns ={'Unnamed: 0': 'Patient'})
 	data = data.set_index('Patient')
 	return data

def fit_lifelines_model(data):
 	cph = CoxPHFitter()
 	model = cph.fit(data, duration_col= 'age_censor', event_col='breastcancer')
 	return model 

def get_covariate_groups(model, covariate, val_range):
    axes = model.plot_covariate_groups(covariate, values=val_range, cmap='coolwarm')
    lines = axes.lines
    axes.clear()
    return {i.get_label(): i.get_data() for i in lines}

    

def get_partial_hazard_ratio(model):
    axes = model.plot(hazard_ratios = True)
    covs = model.summary.index
    lines = axes.get_lines()
    vlines = pd.DataFrame([e.get_data()[0] for e in lines], columns = covs)
    vlines['data_labels'] = ['target', 'lower_bound', 'upper_bound']
    
    vlines = vlines.set_index('data_labels')
    axes.clear()
    return {col: sorted(vlines[col]) for col in vlines.columns}


def load_model():
    with open("BRCA2_model.pickle", "rb") as input_file:
        model = pickle.load(input_file) 
        return model

