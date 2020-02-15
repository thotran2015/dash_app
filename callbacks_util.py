#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 20:31:27 2020

@author: thotran
"""
import pandas as pd
import numpy as np
import pickle 
from process_input import id_variant


#####################################
##### LOAD COXPH MODEL OBJECT #######
#####################################


#BREAST_PAR = ['Nonsense', 'Frameshift', 'Insertion/Deletion', 'Silent', 'Transition',
       # 'Transversion', 'CpG Removing', 'CpG Creating', 'Splice Affecting',
       # 'PRS', 'PC1', 'PC2', 'PC3', 'PC4', 'Family History', 'Region 1',
       # 'Region 2', 'Region 3', 'Region 4', 'Region 5']


def load_model(model_loc):
    with open(model_loc, "rb") as input_file:
        model = pickle.load(input_file) 
        return model

#####################################
###### SURVIVAL FUNCTION PLOT #######
#####################################


def get_survival_prob(model, patient_data):
    return model.predict_survival_function(patient_data)['patient'].to_dict()



def get_patient_data(model):
    input_pars = model.summary.index
    data_info = {par: 1 for par in input_pars}
    return pd.DataFrame(data_info, index = ['patient'])


def get_survival_callback(tab, model):
    patient_data = get_patient_data(model)
    surv = get_survival_prob(model, patient_data)
    baseline = model.baseline_survival_['baseline survival'].to_dict()
    def plot_survival_func():
        data = [
        {'x': list(baseline.keys()), 'y': list(baseline.values()), 'type': 'line', 'name': 'baseline', 'marker': dict(color='rgb(55, 83, 109)') },
                
        {'x': list(surv.keys()), 'y': list(surv.values()), 'type': 'line', 'name': 'individual', 'marker': dict(color='rgb(26, 118, 255)') }
            ]
        return {
            'data': data,
            'layout': {
                    'title': 'Survival Probability of '+ tab,
                    'xaxis': {
                        'title': 'Age',
                        'type': 'linear' 
                    },
                    'yaxis' : {
                        'title': 'Survival Probability',
                        'type': 'linear' 
                    },
                },}
    return plot_survival_func


#####################################
###### PARTIAL HARZARD RATIO PLOT ###
#####################################


def get_partial_hazard_ratio(model, low_95= 'lower 0.95', high_95 = 'upper 0.95', exp_coef = 'exp(coef)'):
    lower = model.summary[low_95]
    upper = model.summary[high_95]
    target = model.summary[exp_coef]
    df = pd.DataFrame([lower, target, upper])
    return {col: list(df[col].values) for col in df.columns}

def get_ph_ratios_callback(model):
    ph_ratios = get_partial_hazard_ratio(model)
    default_covs = model.summary.index[0:3]
    default_covs2 = model.summary.index[3:6]
    def fill_ph_ratios_plot(ph_data, title):
        return {'data': ph_data,
                 'layout': { 
                     'title' : 'PH of '+  title,
                     'xaxis': {
                         'title': 'HR',
                         'type': 'linear' 
        
                         },
                     'yaxis' : {
                         'type': 'category' 
        
                         },
                     }} 

    def plot_box_plot_coef(covs = default_covs, covs2 = default_covs2):
        ph_data = [
          {'x': xy, 'y': [i]*len(xy), 'type': 'scatter', 'name': i, 'mode':'lines+markers',
              } for i, xy in ph_ratios.items() if i in covs
          ]
        ph_data1 = [
          {'x': xy, 'y': [i]*len(xy), 'type': 'scatter', 'name': i, 'mode':'lines+markers',
              } for i, xy in ph_ratios.items() if i in covs2
          ]
        return fill_ph_ratios_plot(ph_data, ', '.join(covs)), fill_ph_ratios_plot(ph_data1, ', '.join(covs2))
    return plot_box_plot_coef


#####################################
###### COVARIATE GROUPS PLOT ########
#####################################
    
def get_plot_layout(title, xlabel, ylabel):
    return { 
            'title' : title,
            'xaxis': {
                'title': xlabel,
                'type': 'linear' 
                },
            'yaxis' : {
                'title': ylabel,
                'type': 'linear' 
                },
            }

def get_covariate_groups(model, covariate, val_range):
    axes2 = model.plot_covariate_groups(covariate, values=val_range, cmap='coolwarm', label = 'covs', plot_baseline=False)
    lines = axes2.get_lines()
    axes2.clear()
    return {i.get_label(): i.get_data() for i in lines}

# model_loc = './models/BRCA2_10_31.pickle'
# MODEL = load_model(model_loc)

# covariates = ['log Allele Frequency', 'Phylop', 'GERP', 'CADD', 'Missense',
#        'Nonsense', 'Frameshift', 'Insertion/Deletion', 'Silent', 'Transition',
#        'Transversion', 'CpG Removing', 'CpG Creating', 'Splice Affecting',
#        'PRS', 'PC1', 'PC2', 'PC3', 'PC4', 'Family History', 'Region 1',
#        'Region 2', 'Region 3', 'Region 4', 'Region 5']
# #'PRS':np.arange(-5, 6, 5), 'Family History': np.arange(0,2), 'Family History': np.arange(0,2), 'Family History': np.arange(0,2
# cov_val_range = {'log Allele Frequency': np.arange(5e-5, 1e-4), 'Phylop': np.arange(0, 2), 
#                  'GERP': np.arange(-5, 6, 5), 'CADD': np.arange(-5, 6, 5), 'Missense': np.arange(0, 2),
#        'Nonsense': np.arange(0, 2), 'Frameshift': np.arange(0, 2) , 'Insertion/Deletion': np.arange(0, 2), 
#        'Silent': np.arange(0,2), 'Transition': np.arange(-5, 6, 5),
#        'Transversion': np.arange(0, 2), 'CpG Removing': np.arange(0, 2), 'CpG Creating': np.arange(0, 2), 
#        'Splice Affecting': np.arange(0, 2), 'PRS': np.arange(-3, 3), 'PC1': np.arange(-18, -7, 2),
#        'PC2': np.arange(0, 6, 2), 'PC3': np.arange(-5, 1, 2), 'PC4': np.arange(-3, 6, 2), 
#        'Family History': np.arange(0,2), 'Region 1': np.arange(0,2),
#        'Region 2': np.arange(0,2), 'Region 3': np.arange(0,2), 'Region 4': np.arange(0,2), 'Region 5': np.arange(0,2)}

# print(MODEL.plot_covariate_groups('Region 5', values= np.arange(0,2), cmap='coolwarm', label = 'covs'))
#print(get_covariate_groups(MODEL, 'Family History', np.arange(0,2)))
def get_covariate_grps_callback(cov, val_range, model):
    covariate= cov
    if cov =='type':
        covariate= ['Silent', 'Nonsense', 'Frameshift', 'Insertion/Deletion']
    
    covariate_groups = get_covariate_groups(model, covariate, val_range= val_range)
    def fill_covariate_groups(cov_data, layout):
        return {'data': cov_data,
                'layout': layout
                }  
    def plot_covariate_groups():
        cov_data = [
             {'x': xy[0], 'y': xy[1], 'type': 'line', 'name': label, }
             for i, (label, xy) in enumerate(covariate_groups.items())
             ]
        layout = get_plot_layout('Survival based on '+ cov, 'Age', 'HR')
        return fill_covariate_groups(cov_data,layout)
    return plot_covariate_groups