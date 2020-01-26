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

#data = get_patient_profiles('./data/patient_profiles.csv')
#model = fit_lifelines_model(data)
#print(get_covariate_groups(model)['PRS=5'])

#print(model.baseline_survival_)
#plot = model.plot_covariate_groups('PRS', values=np.arange(-5, 6, 5), cmap='coolwarm')
#print(model.predict_survival_function(data.head(1)))
#x, y = plot.lines[-1].get_data()
#y = plot.lines[0].get_ydata()
#fig = tpl.figure()
#fig.plot(x, y, label="data", width=50, height=15)
#fig.show()
#print(y)
#plt.plot(x,y, 'ro')
#plt.xlabel('entry a')
#plt.ylabel('entry b')
#plt.show()
#print(x,y)
#for i in range(len(plot.lines)):
#    print(plot.lines[i].get_data())
