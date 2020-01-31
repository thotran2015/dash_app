#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 14:22:48 2020

@author: thotran
"""

GENE_TO_CHROM = {'BRCA1' : 17, 'BRCA2' : 13, 'MSH2': 2, 'MSH6': 2, 'PMS2' : 7, 'MLH1': 9, 'LDLR': 19 , 'APOB': 2, 'PCSK9':1}
import requests

def request_var_data(variant):
    #vep_server = "https://rest.ensembl.org"
    vep_server = "https://grch37.rest.ensembl.org/"
    ext = "/vep/human/hgvs/"
    reg_ext = "/vep/human/region/"
    ##reg_variant = "1:156084729:156084729:1/A"
    ##
    ###"1:6524705:6524705/T?"
    #s_variant = '9:g.22125504G>C'
    #variant = '1:g.156084756C>T'
    reg_variant = "1:156084756:156084756:1/A"
    #'1:g.156084729G>A'
    ##AGT:c.803T>C
    ##opt_par ='?CADD=1?'
    api_url = vep_server+ext+variant
    api_url_ext = vep_server + reg_ext + reg_variant
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
    
def format_variant_id(gene, n_pos, alt, gene_to_chrom = GENE_TO_CHROM, ens = ':g.'):
    var_id =  str(gene_to_chrom[gene]) + ens + str(n_pos) + alt.replace('-','>')
    reg_var_id = str(gene_to_chrom[gene]) + ':'+ str(n_pos)+':' + str(n_pos)+':1/A'
    return var_id


def extract_counters(variant, counters):
    data = request_var_data(variant)
    return {c: data.get(c, None) for c in counters}
    
    