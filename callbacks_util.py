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



GENE_TO_CHROM = {'BRCA1' : 17, 'BRCA2' : 13, 'MSH2': 2, 'MSH6': 2, 'PMS2' : 7, 'MLH1': 3, 'LDLR': 19 , 'APOB': 2, 'PCSK9':1}
CONSEQ = {"Silent", "Nonsense", "Missense", "Deletion", "Frameshift", "Insertion/Deletion"}
POLYGENETIC_OPTIONS = ['Family History', 'obese']
GENE_TO_DISEASE = {'BC': ['BRCA1', 'BRCA2'], 'CC': ['MSH2', 'MSH6', 'PMS2', 'MLH1'], 'CAD': ['LDLR', 'APOB', 'PCSK9']}
########################################
###### Phenotypes Constants ############
########################################
PHENOTYPE_FILE = './data/phenotypes.json'
PHENOTYPE_PAR = {'BC': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_breastcancer'],
                'CC': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_ibd']}
COVS1 = ['sex', 'Family History', 'PRS']
COVS2 = ['Region 1', 'Region 2', 'Region 3', 'Region 4', 'Region 5']
COVS3 = ['Missense', 'Silent', 'Nonsense', 'Frameshift', 'Insertion/Deletion']
COVS4 = ['log Allele Frequency', 'Phylop', 'GERP', 'CADD']

MUT_TYPES = ['Missense', 'Silent', 'Nonsense', 'Frameshift', 'Insertion/Deletion']

#####################################
##### LOAD COXPH MODEL OBJECT #######
#####################################

def load_model(model_loc):
    with open(model_loc, "rb") as input_file:
        model = pickle.load(input_file) 
        return model


        
    
#####################################
###### PROCESS PATIENT DATA #########
#####################################
        
VEP38_URL = 'https://rest.ensembl.org/vep/human/hgvs/'
VEP37_URL = "https://grch37.rest.ensembl.org/vep/human/hgvs/"
        

    
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

#####################################
###### SURVIVAL FUNCTION PLOT #######
#####################################
        
def get_survival_callback(dis_tab, gene, mut_type, chrom, start, end, ref, alt, obese_hist, sex, prs, model): 
    pat_data = pi.get_pat_data(gene, mut_type, chrom, start, end, ref, alt, dis_tab, sex , obese_hist, VEP37_URL)
    model_input = pi.process_patient_data(pat_data, model).fillna(0)
    surv = model.predict_survival_function(model_input)[0]
    baseline = model.baseline_survival_['baseline survival']
    def plot_survival_func():
        data = [
        {'x': baseline.keys(), 'y': baseline.values, 'type': 'line', 'name': 'baseline', 'marker': dict(color='rgb(55, 83, 109)') },
        {'x': surv.keys(), 'y': surv.values, 'type': 'line', 'name': 'individual', 'marker': dict(color='rgb(26, 118, 255)') }
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
###### HAZARD RATIO PLOT ###
#####################################


def get_hazard_ratio(model, exp_coef = 'exp(coef)'):
    lower_upper = model.confidence_intervals_
    target = model.summary.get(exp_coef)
    df = pd.DataFrame([np.exp(lower_upper.iloc[:,0]), target, np.exp(lower_upper.iloc[:,1])])
    return {col: list(df[col].values) for col in df.columns}

def get_hazard_ratios_callback(model):
    ph_ratios = get_hazard_ratio(model)
    cov_grps = [COVS1, COVS2, COVS3, COVS4]
    def fill_ph_ratios_plot(ph_data, title):
        return {'data': ph_data,
                 'layout': { 
                     'title' : title,
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
              {'x': [xy[1]], 'y': [i], 'type': 'scatter', 'name': i, 'mode':'markers', 'showlegend': False,
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
            'title' : title,
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
        pat_label = 'Patient\'s: ' + str(model_input[mut_types].idxmax())
        cov_grps = pd.DataFrame(model_input, columns = [pat_label])
        for val in mut_types:
            cov_grps[val] = cov_grps[pat_label]
            cov_grps[val][mut_types] = 0
            cov_grps[val][val] = 1
        return model.predict_survival_function(cov_grps.T)
    else:
        pat_label = 'Patient\'s: ' + str(round(model_input[covariate], 2))
        cov_grps = pd.DataFrame(model_input, columns = [pat_label])
        for val in val_range:
            cov_grps[covariate + '=' + str(val)] = cov_grps[pat_label]
            cov_grps[covariate + '=' + str(val)][covariate] = val
        return model.predict_survival_function(cov_grps.T)
    



def get_covariate_grps_callback(covariate, val_range, dis_tab, gene, mut_type, chrom, start, end, ref, alt, obese_hist, sex, prs, model):
    pat_data = pi.get_pat_data(gene, mut_type, chrom, start, end, ref, alt, dis_tab, sex , obese_hist, VEP37_URL)
    model_input = pi.process_patient_data(pat_data, model).fillna(0)
    covariate_groups = get_covariate_groups(model, model_input, covariate, val_range= val_range)
    print(covariate_groups)
    
    def fill_covariate_groups(cov_data, layout):
        return {'data': cov_data,
                'layout': layout
                }  
    def plot_covariate_groups():
        cov_data = [
             {'x': covariate_groups.index, 'y': covariate_groups[cov_val], 'type': 'line', 'name':str( cov_val)}
             for cov_val in covariate_groups.columns
             ]
        layout = get_plot_layout('Survival based on '+ covariate, 'Age', 'Survival Probability')
        return fill_covariate_groups(cov_data,layout)
    return plot_covariate_groups




# def process_model_input(dis_tab, gene, n_pos, alt, obese_hist, prs, model):
#     variant = id_variant(gene, n_pos, alt)
#     var_args = extract_var_covs_from_VEP(variant)
#     input_args = get_polygenetic_input(dis_tab, obese_hist, gene, prs)
#     phenotype_args = get_phenotypes(dis_tab)
#     all_args = {**var_args, **input_args, **phenotype_args}
#     labels = model.summary.index
#     data = [float(all_args.get(i, 0)) for i in labels]
#     df = pd.DataFrame({'patient': data})
#     df['labels'] = labels
#     df = df.set_index('labels').T
#     return df



# def set_mutation_type_binary_vector(var_type, mut_types = MUTATION_TYPES, conseq = CONSEQ):
#     mut_type = mut_types.get(var_type, 'Other')
#     return {c: 1 if c == mut_type else 0 for c in conseq}

# def get_survival_prob(model, patient_data):
#     return model.predict_survival_function(patient_data)['patient'].to_dict()


# def id_variant(gene, n_pos, alt, gene_to_chrom = GENE_TO_CHROM):
#     #'17:g.41197701G>A'
#     return str(gene_to_chrom[gene]) + ':g.' + str(n_pos) + alt

# def request_var_data(variant):
#     vep_server = "https://grch37.rest.ensembl.org/"
#     ext = "/vep/human/hgvs/"
#     api_url = vep_server+ext+variant+ '?Conservation=1&CADD=1&canonical=1'
#     try:
#         r = requests.get(api_url, headers={ "Content-Type" : "application/json"}, verify=False, timeout=5)
#         if not r.ok:
#             return "Bad request"
#         decoded = r.json()[0]
#         return decoded
#     except requests.exceptions.Timeout:
#         return "timeout"

# def extract_var_covs_from_VEP(variant, counters = ['most_severe_consequence', 'transcript_consequences', 'colocated_variants']):
#     info = {}
#     data = request_var_data(variant)
#     extracted = {c: data.get(c, None) for c in counters}
#     can_trans =[t for t in extracted['transcript_consequences'] if 'canonical' in t] 
#     if can_trans:
#         info['CADD'] = can_trans[0].get('cadd_raw', 0.5)
#         info['GERP'] = can_trans[0].get('conservation', 0.5)
#         var_type = can_trans[0]['consequence_terms'][0]
#         info.update(set_mutation_type_binary_vector(var_type))
#     else:
#         info['CADD'] = 0
#         info['GERP'] = 0
#         info.update(set_mutation_type_binary_vector('Other'))
#     freq = float(extracted['colocated_variants'][0]['frequencies']['A']['gnomad']) 
#     info['log Allele Frequency'] = -np.log10(freq)
#     if info['log Allele Frequency']== 0.0:
#         info['log Allele Frequency'] = 3e-6

#     return info
    
        #[for val in val_range]
           
        #axes2 = model.plot_covariate_groups(covariate, values=val_range, cmap='coolwarm', label = 'covs', plot_baseline=False)
        #lines = axes2.get_lines()
        #axes2.clear()
        
        #print('covs:', model.predict_survival_function(covariate))
    #return {i.get_label(): i.get_data() for i in lines}


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