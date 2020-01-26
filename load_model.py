#import pickle 
#import scipy
#import lifelines

# from lifelines import CoxPHFitter 
# import pandas as pd
# #import numpy as np
# #import termplotlib as tpl
# #import matplotlib.pyplot as plt

# def get_patient_profiles(file):
# 	data = pd.read_csv(file).rename(columns ={'Unnamed: 0': 'Patient'})
# 	data = data.set_index('Patient')
# 	return data

# def fit_lifelines_model(data):
#  	cph = CoxPHFitter()
#  	model = cph.fit(data, duration_col= 'age_censor', event_col='breastcancer')
#  	return model 

# def get_covariate_groups(model, covariate, val_range):
#     axes = model.plot_covariate_groups(covariate, values=val_range, cmap='coolwarm')
#     lines = axes.lines
#     axes.remove()
#     return {i.get_label(): i.get_data() for i in lines}

# def get_covariate_multi_grps(model, covariate_list, val_range):
#     axes = model.plot_covariate_groups(covariate_list, values=val_range, cmap='coolwarm')
#     lines = axes.lines
#     axes.remove()
#     return {i.get_label(): i.get_data() for i in lines}
    



# def load_model():
# 	with open("BRCA2_model.pickle", "rb") as input_file:
# 		model = pickle.load(input_file) 
# 		#print(model.hazards_)
# 		return model
#ex_model = load_model()

