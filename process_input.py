#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 14:22:48 2020

@author: thotran
"""
import requests
import pandas as pd
import numpy as np

GENE_TO_CHROM = {'BRCA1' : 17, 'BRCA2' : 13, 'MSH2': 2, 'MSH6': 2, 'PMS2' : 7, 'MLH1': 9, 'LDLR': 19 , 'APOB': 2, 'PCSK9':1}
GENE_TO_DISEASE = {'BC': ['BRCA1', 'BRCA2'], 'CC': ['MSH2', 'MSH6', 'PMS2', 'MLH1'], 'CAD': ['LDLR', 'APOB', 'PCSK9']}

MUTATION_TYPES = {'synonymous_variant':'Silent', 'missense_variant': 'Missense', 'nonsense_variant':'Nonsense'}
CONSEQ = {"Silent", "Nonsense", "Missense", "Deletion", "Frameshift", "Insertion/Deletion"}

POLYGENETIC_OPTIONS = ['fam_hist', 'obese']

BREAST_PAR = ['Nonsense', 'Frameshift', 'Insertion/Deletion', 'Silent', 'Transition',
       'Transversion', 'CpG Removing', 'CpG Creating', 'Splice Affecting',
       'PRS', 'PC1', 'PC2', 'PC3', 'PC4', 'Family History', 'Region 1',
       'Region 2', 'Region 3', 'Region 4', 'Region 5']
#["gps_breastcancer", "fam_hist", "allele_frequency", "Silent", "Nonsense", "Missense", "Deletion", "Frameshift"]
COLREC_PAR = [ "PRS", "MSH2", "MSH6" , "MLH1" , "PMS2" , "fam_hist" , "allele_frequency" , "PC1" , "PC2" , "PC3" ,
    "PC4" , "gps_ibd", "Missense" , "Nonsense" , "Frameshift" , "Insertion/Deletion" ]
COR_ARTERY_PAR = []

INPUT_PAR ={'BC': BREAST_PAR, 'CC':COLREC_PAR, 'CAD': COR_ARTERY_PAR }

########################################
###### Phenotypes Constants ############
########################################
PHENOTYPE_FILE = './data/phenotypes.json'
PHENOTYPE_PAR = {'BC': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_breastcancer'],
                'CC': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_ibd']}

##################################################
###### Process Variant Input from VEP ############
##################################################

def set_mutation_type_binary_vector(var_type, mut_types = MUTATION_TYPES, conseq = CONSEQ):
    mut_type = mut_types.get(var_type, 'Other')
    return {c: 1 if c == mut_type else 0 for c in conseq}

 

def id_variant(gene, n_pos, alt, gene_to_chrom = GENE_TO_CHROM):
    #'17:g.41197701G>A'
    return str(gene_to_chrom[gene]) + ':g.' + str(n_pos) + alt

def request_var_data(variant):
    #vep_server = "https://rest.ensembl.org"
    vep_server = "https://grch37.rest.ensembl.org/"
    ext = "/vep/human/hgvs/"
    api_url = vep_server+ext+variant+ '?Conservation=1&CADD=1&canonical=1'
    #api_url_ext = vep_server + reg_ext + reg_variant
    try:
        r = requests.get(api_url, headers={ "Content-Type" : "application/json"}, verify=False, timeout=5)
        if not r.ok:
            return "Bad request"
            #r.raise_for_status()
             #sys.exit()
            #return "Bad request"
        decoded = r.json()[0]
        #return decoded['id'], decoded['most_severe_consequence']
        return decoded
    except requests.exceptions.Timeout:
        return "timeout"



def extract_counters(variant, counters):
    data = request_var_data(variant)
    #print(data)
    return {c: data.get(c, None) for c in counters}
    
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
    #df = access_dropbox_file(phenotype_file)
    df = pd.read_json(phenotype_file)
    if disease in PHENOTYPE_PAR:
        return df[PHENOTYPE_PAR[disease]].apply(pd.to_numeric).mean(axis = 0, skipna = True)
    else:
        return 'No Data in Phenotype File'


##################################################
###### Process User Input from Interface #########
##################################################
        
def process_model_input(variant, disease, model, var_args, input_args, phenotype_args = dict()):
    var_args = extract_var_covs_from_VEP(variant)
    all_args = {**var_args, **input_args, **phenotype_args}
    data = [0 for i in INPUT_PAR[disease]]
    #data = [float(all_args[i]) for i in INPUT_PAR[disease]]
    labels = model.summary.index
    df = pd.DataFrame({'patient': data})
     
    df['labels'] = labels
    df = df.set_index('labels').T
    df['GERP'] = -5
    df['PRS'] = all_args['PRS']
 
    return df.drop(columns = ['Silent'])
        
    
    