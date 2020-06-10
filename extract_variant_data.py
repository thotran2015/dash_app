#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 15:48:59 2020

@author: thotran
"""
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




import numpy as np

MUT_TYPES = ['Missense', 'Silent', 'Nonsense', 'Frameshift', 'Insertion/Deletion']
REGIONS = ['Region 1', 'Region 2', 'Region 3','Region 4', 'Region 5']
    

def extract_raw_variant_attributes(data, gene, alt):
    info = {}
    canonical_transcript = [t for t in data.get('transcript_consequences', []) if 'canonical' in t and t['gene_symbol']==gene] 
    if canonical_transcript:
        info['CADD'] = canonical_transcript[0].get('cadd_raw', 0)
        info['GERP'] = canonical_transcript[0].get('gerp++_rs', 0)
        info['Phylop'] = canonical_transcript[0].get('phylop100way_vertebrate', 0)
        info['consequence'] = canonical_transcript[0].get('consequence_terms', 'Other')
        info['trans_pos'] = (canonical_transcript[0].get('cds_start', 0), canonical_transcript[0].get('cds_end', 0))
    else:
        print('Canonical transcript not found')
        info['CADD'], info['GERP'], info['Phylop'], info['consequence'], info['trans_pos'] = 0, 0, 0, '', (0,0)

    colocated_variant = [var for var in data.get('colocated_variants', []) if 'frequencies' in var]
    if colocated_variant:
        freq = float(colocated_variant[0]['frequencies'].get(alt, {}).get('gnomad', 0))
        info['log Allele Frequency'] = -np.log10(freq)
        if info['log Allele Frequency'] == 0.0:
            info['log Allele Frequency'] = 3e-6
    else:
        print('Allele frequencies not found')
        info['log Allele Frequency'] = 3e-6
    return info

##################################################
###### Process Variant Input from VEP ############
##################################################

def one_hot_mutation_type(mut_type):
    return {c: 1 if c == mut_type else 0 for c in MUT_TYPES}
    
def define_region(trans_pos, gene_bounds):
    closest_pos = min(gene_bounds, key = lambda list_val: abs(list_val - trans_pos))
    region = gene_bounds.index(closest_pos)
    return {reg: 1 if i==region else 0 for i, reg in enumerate(REGIONS)}

def tranversion_transition(ref, alt):
    if ref in {'A', 'G'} and alt in {'A', 'G'}:
        return {'Transition': 1, 'Transversion': 0}
    elif ref in {'C', 'T'} and alt in {'C', 'T'}:
        return {'Transition': 1, 'Transversion': 0}
    else:
        return {'Transition': 0, 'Transversion': 1}

def splicing_effect(var_attr):
    for conseq in var_attr['consequence']:
        if 'splice' in conseq:
            return {'Splice Affecting': 1}
    return {'Splice Affecting': 0}

def extract_variant_attributes(data, gene, mut_type, ref, alt):
    var_attr = extract_raw_variant_attributes(data, gene, alt)
    var_attr.update(one_hot_mutation_type(mut_type))
    var_attr.update(define_region(var_attr['trans_pos'][0], GENE_TO_BOUNDARIES[gene]))
    var_attr.update(tranversion_transition(ref, alt))
    var_attr.update(splicing_effect(var_attr))
    return var_attr
