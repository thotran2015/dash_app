#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 12:22:55 2020

@author: thotran
"""


VEP38_URL = 'https://rest.ensembl.org/vep/human/hgvs/'
VEP37_URL = "https://grch37.rest.ensembl.org/vep/human/hgvs/"

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


MUT_TYPES = ['Missense', 'Silent', 'Nonsense', 'Frameshift', 'Insertion/Deletion']
REGIONS = ['Region 1', 'Region 2', 'Region 3','Region 4', 'Region 5']



PERSONAL = ['sex', 'Family History', 'PRS']
REGIONS = ['Region 1', 'Region 2', 'Region 3', 'Region 4', 'Region 5']
MUT_TYPES = ['Missense', 'Silent', 'Nonsense', 'Frameshift', 'Insertion/Deletion', 'Insertion', 'Deletion']
VAR_ATTR = ['log Allele Frequency', 'Phylop', 'GERP', 'CADD']