#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 14:22:48 2020

@author: thotran
"""
import pickle
import pandas as pd

import query_variant_data as q
import extract_variant_data as ev
import extract_individual_data as ei


VEP38_URL = 'https://rest.ensembl.org/vep/human/hgvs/'
VEP37_URL = "https://grch37.rest.ensembl.org/vep/human/hgvs/"

BC_PAR = ['log Allele Frequency', 'Phylop', 'GERP', 'CADD', 'Missense',
       'Nonsense', 'Frameshift', 'Insertion/Deletion', 'Silent', 'Transition',
       'Transversion', 'CpG Removing', 'CpG Creating', 'Splice Affecting',
       'PRS', 'PC1', 'PC2', 'PC3', 'PC4', 'Family History', 'Region 1',
       'Region 2', 'Region 3', 'Region 4', 'Region 5']

COLREC_PAR = [ "PRS", "MSH2", "MSH6" , "MLH1" , "PMS2" , "fam_hist" , "allele_frequency" , "PC1" , "PC2" , "PC3" ,
    "PC4" , "gps_ibd", "Missense" , "Nonsense" , "Frameshift" , "Insertion/Deletion" ]
COR_ARTERY_PAR = []

INPUT_PAR ={'BC': BC_PAR, 'CC':COLREC_PAR, 'CAD': COR_ARTERY_PAR }



##################################################
###### Process Variant Input from VEP ############
##################################################
VEP38_URL = 'https://rest.ensembl.org/vep/human/hgvs/'
VEP37_URL = "https://grch37.rest.ensembl.org/vep/human/hgvs/"


def get_variant_data(gene, n_pos, alt, vep_url):
    variant = q.id_variant(gene, n_pos, alt)
    data = q.request_var_data(variant, vep_url)
    if data == 'timeout':
        print(data)
    covariates = ev.extract_variant_attributes(data)
    return pd.Series(covariates)

def get_pat_data(gene, n_pos, alt, disease, sex, other, vep_url):
    variant = q.id_variant(gene, n_pos, alt)
    data = q.request_var_data(variant, vep_url)
    if data == 'timeout':
        print(data)
    covariates = ev.extract_variant_attributes(data)
    ind = ei.extract_ind_data(disease, other, gene, sex)
    pat_data = {**covariates, **ind}
    return pat_data


##########################################
###### Process Patient For Model #########
##########################################
        
def process_patient_data(pat_data, model):
    pars = model.summary.index
    data = {p: pat_data.get(p, None) for p in pars}
    return pd.Series(data)



# Example 1: Get Raw Unprocessed Data from VEP
variant = q.id_variant('MLH1', 37070280, 'G>A')
data = q.request_var_data(variant, VEP37_URL)
print(data)
    

# Example 2: Get pre-processed variant data 
print(get_variant_data('MLH1', 37070280, 'G>A', VEP37_URL))
    
        
    
#Example 3: Get processed, complete patient data for model
#### Uncomment to see result #####
# MLH1_model = './models/MLH1_model.pickle'
# with open(MLH1_model, 'rb') as m:
#     model = pickle.load(m)
    
# pat_data = get_pat_data('MLH1', 37070280, 'G>A', 'CC', 'F', ['Family History', 'obese'], VEP37_URL)
# pat_df = process_patient_data(pat_data, model)
# print(pat_df)