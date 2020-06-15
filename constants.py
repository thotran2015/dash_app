#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 12:22:55 2020

@author: thotran
"""


VEP38_URL = 'https://rest.ensembl.org/vep/human/hgvs/'
VEP37_URL = "https://grch37.rest.ensembl.org/vep/human/hgvs/"
EXT = '/?CADD=1&canonical=1&dbNSFP=phyloP100way_vertebrate,GERP%2B%2B_RS'

REDIS_URL = 'redis://h:pd130aee8e46d7b6b6956ab4de6847b77b400cc05461d0540d235c495efb1e4f2@ec2-34-202-45-193.compute-1.amazonaws.com:9609'
DATABASE_URL = 'postgres://duozofkhzsfjvy:46ef1e44c2b9751801126174b41e124a7f1c847b9e0cf2f27af49a0a3278d5db@ec2-54-235-89-123.compute-1.amazonaws.com:5432/da1e3uq86ab5tu'



#disease and their code names
DISEASES = {'BC': 'Breast Cancer', 'CC': 'Colorectal Cancer', 'CAD': 'Coronary Artery Disease'}

GENE_TO_CHROM = {'BRCA1' : 17, 'BRCA2' : 13, 'MSH2': 2, 'MSH6': 2, 'PMS2' : 7, 'MLH1': 3, 'LDLR': 19 , 'APOB': 2, 'PCSK9':1}
GENE_TO_DISEASE = {'BC': ['BRCA1', 'BRCA2'], 'CC': ['MSH2', 'MSH6', 'PMS2', 'MLH1'], 'CAD': ['LDLR', 'APOB', 'PCSK9']}

LDLR = [0, 431, 829, 1343, 1886, 2579]
APOB = [0, 1830, 5116, 7605, 10238, 13679]
PCSK9 = [0, 42, 286, 426, 1120, 2054]
BRCA1 = [0, 966, 2028, 3188, 4427, 5560.0]
BRCA2 = [0, 2049, 4058, 5879, 7738, 10171]
MLH1 = [0, 322, 739, 1246, 1778, 2269.0]
MSH2  = [0, 565, 1077, 1594, 2152, 2801]
MSH6 = [0, 973, 1714, 2550, 3377, 4077]
PMS2 = [0, 445, 1036, 1532, 2016, 2458.0]

GENE_TO_BOUNDARIES = {'BRCA1' : BRCA1, 'BRCA2' : BRCA2, 'MSH2': MSH2, 'MSH6': MSH6, 'PMS2' : PMS2, 'MLH1': MLH1, 'LDLR': LDLR , 'APOB': APOB, 'PCSK9':PCSK9}


REGIONS = ['Region 1', 'Region 2', 'Region 3','Region 4', 'Region 5']



PERSONAL = ['sex', 'Family History', 'PRS']
REGIONS = ['Region 1', 'Region 2', 'Region 3', 'Region 4', 'Region 5']
MUT_TYPES = ['Missense', 'Silent', 'Nonsense', 'Frameshift', 'Insertion/Deletion', 'Insertion', 'Deletion']
VAR_ATTR = ['log Allele Frequency', 'Phylop', 'GERP', 'CADD']

#parameter value range for each covariate group
COV_DISEASE = {'BC': ['Family History', 'log Allele Frequency', 'Mutations', 'Regions'],
               'CC':  ['Family History', 'log Allele Frequency', 'Mutations', 'Regions'],
               'CAD' : ['Family History', 'log Allele Frequency', 'Mutations', 'Regions']}



COV_DISEASE_ROWS = {'breast cancer': [['Family History', 'log Allele Frequency'], ['Mutations', 'Regions']],
               'colorectal cancer':  [['Family History', 'log Allele Frequency'], ['Mutations', 'Regions']],
               'coronary artery disease' : [['Family History', 'log Allele Frequency'], ['Mutations', 'Regions']]}