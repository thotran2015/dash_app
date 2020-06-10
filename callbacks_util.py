#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 20:31:27 2020

@author: thotran
"""
import pandas as pd
import pickle 
import process_input as pi
import numpy as np
from constants import VEP37_URL, GENE_TO_BOUNDARIES, DISEASES
from constants import PERSONAL, REGIONS, MUT_TYPES, VAR_ATTR

def label_region(gene):
    reg_bounds = GENE_TO_BOUNDARIES[gene]
    return {'Region '+ str(i+1): 'Region ' + str(i+1) + ' ('+ str(reg_bounds[i]) + '-'+ str(e) +')' for i, e in enumerate(reg_bounds[1:])}



SEXES = {0: 'Female', 1: 'Male'}
FAM_HIST = {0: 'No Family History', 1: 'Family History'}
COV_GRP_LABELS = {'sex': SEXES, 'Family History': FAM_HIST}

#####################################
##### LOAD COXPH MODEL OBJECT #######
#####################################

def load_model(model_loc):
    with open(model_loc, "rb") as input_file:
        model = pickle.load(input_file) 
        return model



#####################################
###### SURVIVAL FUNCTION PLOT #######
#####################################
        
def get_survival_callback(dis_tab, gene, mut_type, chrom, start, end, ref, alt, obese_hist, sex, prs, model):
    pat_data = pi.get_pat_data(gene, mut_type, chrom, start, end, ref, alt, dis_tab, sex , obese_hist, VEP37_URL)
    baseline = model.baseline_survival_['baseline survival']
    baseline = baseline[baseline.index >= 0]
    if len(pat_data) == 0:
        def plot_survival_func():
            data = [
            {'x': baseline.keys(), 'y': baseline.values, 'type': 'line', 'name': 'baseline', 'marker': dict(color='rgb(55, 83, 109)') },
                ]
            return {
                'data': data,
                'layout': {
                        'title': 'Survival Probability of '+ DISEASES[dis_tab],
                        'xaxis': {
                            'title': 'Age',
                            'type': 'linear' 
                        },
                        'yaxis' : {
                            'title': 'Survival Probability',
                            'type': 'linear' 
                        },
                    },}
    else:
        model_input = pi.process_patient_data(pat_data, model).fillna(0)
        surv = model.predict_survival_function(model_input)[0]
        surv = surv[surv.index >= 0]
        def plot_survival_func():
            data = [
            {'x': baseline.keys(), 'y': baseline.values, 'type': 'line', 'name': 'baseline', 'marker': dict(color='rgb(55, 83, 109)') },
            {'x': surv.keys(), 'y': surv.values, 'type': 'line', 'name': 'individual', 'marker': dict(color='rgb(26, 118, 255)') }
                ]
            return {
                'data': data,
                'layout': {
                        'title': 'Survival Probability of '+ DISEASES[dis_tab],
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
###### HAZARD RATIO PLOT ###
#####################################


def get_hazard_ratio(model, exp_coef = 'exp(coef)'):
    lower_upper = model.confidence_intervals_
    target = model.summary.get(exp_coef)
    df = pd.DataFrame([np.exp(lower_upper.iloc[:,0]), target, np.exp(lower_upper.iloc[:,1])])
    return {col: list(df[col].values) for col in df.columns}

def get_hazard_ratios_callback(gene, model):
    ph_ratios = get_hazard_ratio(model)
    reg_labels = label_region(gene)
    cov_grps = [PERSONAL, REGIONS, MUT_TYPES, VAR_ATTR]
    def fill_ph_ratios_plot(ph_data, title):
        return {'data': ph_data,
                 'layout': { 
                     'title' : title.title(),
                     'xaxis': {
                         'title': 'Relative Risk or Hazard Ratio',
                         #'type': 'linear',
                         'automargin': True
        
                         },
                     'yaxis' : {
                         'type': 'category',
                         'automargin': True
                         },
                     'legend': {
                         'orientation': 'h',
                         'xanchor':'right',
                         'yanchor':'center'
                         },
                     }} 

    def plot_box_plot_coef(cov_grps = cov_grps):
        ph_ratios_plots = []
        for cov in cov_grps:
            ph_data = [
              {'x': [xy[1]], 'y': [reg_labels.get(i, i)], 'type': 'scatter', 'name': i, 'mode':'markers', 'showlegend': False,
               'error_x': {
                   'type': 'data',
                   'symmetric': False,
                   'array': [xy[2]-xy[0]],
                   'arrayminus':[xy[1]-xy[0]]}, 
                  } for i, xy in ph_ratios.items() if i in cov
              ]
            ph_ratios_plots.append(fill_ph_ratios_plot(ph_data, 'Relative Risk or Hazard Ratio of ' + ', '.join(cov)))
        return ph_ratios_plots
    return plot_box_plot_coef


#####################################
###### COVARIATE GROUPS PLOT ########
#####################################
    
def get_plot_layout(title, xlabel, ylabel):
    return { 
            'title' : title.title(),
            'xaxis': {
                'title': xlabel,
                'type': 'linear' 
                },
            'yaxis' : {
                'title': ylabel,
                'type': 'linear' 
                }
            }


def get_covariate_groups(model, model_input, covariate, val_range):
    if covariate =='Mutations':
        mut_types = list(set(MUT_TYPES) & set(model.summary.index))
        pat_label = 'Patient: ' + str(model_input[mut_types].idxmax())
        cov_grps = pd.DataFrame(model_input, columns = [pat_label])
        for val in mut_types:
            cov_grps[val] = cov_grps[pat_label]
            cov_grps[val][mut_types] = 0
            cov_grps[val][val] = 1
        survival = model.predict_survival_function(cov_grps.T)
        return survival[survival.index>0]
    elif covariate == 'Regions':
        regions = list(set(REGIONS) & set(model.summary.index))
        pat_label = 'Patient: ' + str(model_input[regions].idxmax())
        cov_grps = pd.DataFrame(model_input, columns = [pat_label])
        for val in regions:
            cov_grps[val] = cov_grps[pat_label]
            cov_grps[val][regions] = 0
            cov_grps[val][val] = 1
        survival = model.predict_survival_function(cov_grps.T)
        return survival[survival.index>0]
    else:
        cov_val_label = COV_GRP_LABELS.get(covariate, {})
        pat_val = round(model_input[covariate], 2)
        pat_label = 'Patient: ' + cov_val_label.get(int(pat_val)) if pat_val in cov_val_label else 'Patient: ' + str(pat_val)
        cov_grps = pd.DataFrame(model_input, columns = [pat_label])
        for val in val_range:
            col_name = cov_val_label.get(val) if val in cov_val_label else covariate + ' = ' + str(val)
            cov_grps[col_name] = cov_grps[pat_label]
            cov_grps[col_name][covariate] = val
        survival =  model.predict_survival_function(cov_grps.T)
        return survival[survival.index>0]
    



def get_covariate_grps_callback(covariate, val_range, dis_tab, gene, mut_type, chrom, start, end, ref, alt, obese_hist, sex, prs, model):
    pat_data = pi.get_pat_data(gene, mut_type, chrom, start, end, ref, alt, dis_tab, sex , obese_hist, VEP37_URL)
    if len(pat_data) == 0:
        def plot_covariate_groups():
            return {}  
    else:
        model_input = pi.process_patient_data(pat_data, model).fillna(0)
        covariate_groups = get_covariate_groups(model, model_input, covariate, val_range= val_range)
        def fill_covariate_groups(cov_data, layout):
            return {'data': cov_data,
                    'layout': layout
                    }  
        def plot_covariate_groups():
            cov_data = [
                 {'x': covariate_groups.index, 'y': covariate_groups[cov_val], 'type': 'line', 'name':str(cov_val)}
                 for cov_val in covariate_groups.columns
                 ]
            layout = get_plot_layout('Survival based on '+ covariate, 'Age', 'Survival Probability')
            return fill_covariate_groups(cov_data,layout)
    return plot_covariate_groups



