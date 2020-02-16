#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 20:31:27 2020

@author: thotran
"""
import pandas as pd
import numpy as np
import pickle 
import requests

GENE_TO_CHROM = {'BRCA1' : 17, 'BRCA2' : 13, 'MSH2': 2, 'MSH6': 2, 'PMS2' : 7, 'MLH1': 9, 'LDLR': 19 , 'APOB': 2, 'PCSK9':1}
MUTATION_TYPES = {'synonymous_variant':'Silent', 'missense_variant': 'Missense', 'nonsense_variant':'Nonsense'}
CONSEQ = {"Silent", "Nonsense", "Missense", "Deletion", "Frameshift", "Insertion/Deletion"}
POLYGENETIC_OPTIONS = ['Family History', 'obese']
GENE_TO_DISEASE = {'BC': ['BRCA1', 'BRCA2'], 'CC': ['MSH2', 'MSH6', 'PMS2', 'MLH1'], 'CAD': ['LDLR', 'APOB', 'PCSK9']}
########################################
###### Phenotypes Constants ############
########################################
PHENOTYPE_FILE = './data/phenotypes.json'
PHENOTYPE_PAR = {'BC': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_breastcancer'],
                'CC': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_ibd']}

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
        
    
#####################################
###### PROCESS PATIENT DATA #########
#####################################

def set_mutation_type_binary_vector(var_type, mut_types = MUTATION_TYPES, conseq = CONSEQ):
    mut_type = mut_types.get(var_type, 'Other')
    return {c: 1 if c == mut_type else 0 for c in conseq}

def get_survival_prob(model, patient_data):
    return model.predict_survival_function(patient_data)['patient'].to_dict()


def id_variant(gene, n_pos, alt, gene_to_chrom = GENE_TO_CHROM):
    #'17:g.41197701G>A'
    return str(gene_to_chrom[gene]) + ':g.' + str(n_pos) + alt

def request_var_data(variant):
    vep_server = "https://grch37.rest.ensembl.org/"
    ext = "/vep/human/hgvs/"
    api_url = vep_server+ext+variant+ '?Conservation=1&CADD=1&canonical=1'
    try:
        r = requests.get(api_url, headers={ "Content-Type" : "application/json"}, verify=False, timeout=5)
        if not r.ok:
            return "Bad request"
        decoded = r.json()[0]
        return decoded
    except requests.exceptions.Timeout:
        return "timeout"

def extract_var_covs_from_VEP(variant, counters = ['most_severe_consequence', 'transcript_consequences', 'colocated_variants']):
    info = {}
    data = request_var_data(variant)
    extracted = {c: data.get(c, None) for c in counters}
    
    can_trans =[t for t in extracted['transcript_consequences'] if 'canonical' in t] 
    if can_trans:
        info['CADD'] = can_trans[0]['cadd_raw']
        info['GERP'] = can_trans[0]['conservation']
        var_type = can_trans[0]['consequence_terms'][0]
        info.update(set_mutation_type_binary_vector(var_type))
    else:
        info['CADD'] = 0
        info['GERP'] = 0
        info.update(set_mutation_type_binary_vector('Other'))
    freq = float(extracted['colocated_variants'][0]['frequencies']['A']['gnomad']) 
    info['log Allele Frequency'] = -np.log10(freq)
    if info['log Allele Frequency']== 0.0:
        info['log Allele Frequency'] = 3e-6
    return info


    
##################################################
###### Process User Input from Interface #########
##################################################

def get_polygenetic_input(disease, polygenetic_selected, gene_selected, prs=None):
    polygene = {option: 1 if option in polygenetic_selected else 0 for option in POLYGENETIC_OPTIONS}
    if prs !=None:
        polygene["PRS"] = prs

    for gene in GENE_TO_DISEASE[disease]:
        if gene == gene_selected: 
            polygene[gene] = 1
        else:
            polygene[gene] = 0

    return polygene


##################################################
###### Process Patient Phenotypes like PCs #########
##################################################

def get_phenotypes(disease, phenotype_file = PHENOTYPE_FILE):
    df = pd.read_json(phenotype_file)
    if disease in PHENOTYPE_PAR:
        return df[PHENOTYPE_PAR[disease]].apply(pd.to_numeric).mean(axis = 0, skipna = True)
    else:
        return 'No Data in Phenotype File'


def process_model_input(dis_tab, gene, n_pos, alt, obese_hist, prs, model):
    variant = id_variant(gene, n_pos, alt)
    var_args = extract_var_covs_from_VEP(variant)
    input_args = get_polygenetic_input(dis_tab, obese_hist, gene, prs)
    phenotype_args = get_phenotypes(dis_tab)
    all_args = {**var_args, **input_args, **phenotype_args}
    labels = model.summary.index
    data = [float(all_args.get(i, 0)) for i in labels]
    df = pd.DataFrame({'patient': data})
    df['labels'] = labels
    df = df.set_index('labels').T
    return df


def get_survival_callback(dis_tab, gene, n_pos, alt, obese_hist, prs, model): 
    #patient_data = get_patient_data(dis_tab, gene, n_pos, alt, obese_hist, prs, model)
    pat_data = process_model_input(dis_tab, gene, n_pos, alt, obese_hist, prs, model)
    surv = get_survival_prob(model, pat_data)
    baseline = model.baseline_survival_['baseline survival'].to_dict()
    def plot_survival_func():
        data = [
        {'x': list(baseline.keys()), 'y': list(baseline.values()), 'type': 'line', 'name': 'baseline', 'marker': dict(color='rgb(55, 83, 109)') },
                
        {'x': list(surv.keys()), 'y': list(surv.values()), 'type': 'line', 'name': 'individual', 'marker': dict(color='rgb(26, 118, 255)') }
            ]
        return {
            'data': data,
            'layout': {
                    'title': 'Survival Probability of '+ dis_tab,
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
    chunk_size = len(model.summary.index)//4
    covs1 = model.summary.index[0:chunk_size]
    covs2 = model.summary.index[chunk_size:2*chunk_size]
    covs3 = model.summary.index[2*chunk_size:3*chunk_size]
    covs4 = model.summary.index[3*chunk_size:4*chunk_size]
    cov_grps = [covs1, covs2, covs3, covs4]
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

    def plot_box_plot_coef(cov_grps = cov_grps):
        ph_ratios_plots = []
        for cov in cov_grps:
            ph_data = [
              {'x': xy, 'y': [i]*len(xy), 'type': 'scatter', 'name': i, 'mode':'lines+markers',
                  } for i, xy in ph_ratios.items() if i in cov
              ]
            ph_ratios_plots.append(fill_ph_ratios_plot(ph_data, ', '.join(cov)))
        return ph_ratios_plots
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