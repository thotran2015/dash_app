#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 15:52:27 2020

@author: thotran
"""
import pandas as pd

POLYGENETIC_OPTIONS = ['Family History', 'obese']
GENE_TO_DISEASE = {'BC': ['BRCA1', 'BRCA2'], 'CC': ['MSH2', 'MSH6', 'PMS2', 'MLH1'], 'CAD': ['LDLR', 'APOB', 'PCSK9']}
SEX = {'M': 1, 'F': 0}
########################################
###### Phenotypes Constants ############
########################################
PHENOTYPE_FILE = './data/phenotypes.json'
PHENOTYPE_PAR = {'BC': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_breastcancer'],
                'CC': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_ibd'],
                'CAD': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_cad']}

##################################################
###### Extract User Input from Interface #########
##################################################

def get_polygenetic_input(disease, polygenetic_selected, gene_selected, prs=0):
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
###### Process Patient Phenotypes like PCs #######
##################################################

def get_phenotypes(disease, phenotype_file = PHENOTYPE_FILE):
    df = pd.read_json(phenotype_file)
    if disease in PHENOTYPE_PAR:
        phenos = df[PHENOTYPE_PAR[disease]].apply(pd.to_numeric).mean(axis = 0, skipna = True)
        return phenos.rename(index = {'gps_breastcancer': 'GPS', 'gps_ibd': 'GPS', 'gps_cad': 'GPS'})
    else:
        return 'No Data in Phenotype File'
    
    
def extract_ind_data(disease, polygenetic_selected, gene_selected, sex_selected):
    polygene = get_polygenetic_input(disease, polygenetic_selected, gene_selected)
    pheno = get_phenotypes(disease)
    return {**polygene, **pheno, 'sex': SEX[sex_selected]}
    
    