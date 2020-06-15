#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 15:48:59 2020

@author: thotran
"""

from constants import GENE_TO_BOUNDARIES, MUT_TYPES, REGIONS
import numpy as np


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
        if 'splice_donor_variant' in conseq or 'splice_acceptor_variant' in conseq or 'splice_region_variant' in conseq:
            return {'Splice Affecting': 1}
    return {'Splice Affecting': 0}

def extract_variant_attributes(data, gene, mut_type, ref, alt):
    var_attr = extract_raw_variant_attributes(data, gene, alt)
    var_attr.update(one_hot_mutation_type(mut_type))
    var_attr.update(define_region(var_attr['trans_pos'][0], GENE_TO_BOUNDARIES[gene]))
    var_attr.update(tranversion_transition(ref, alt))
    var_attr.update(splicing_effect(var_attr))
    return var_attr
