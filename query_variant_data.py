#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 10:22:23 2020

@author: thotran
"""
import requests, sys
import json
import os 

#https://rest.ensembl.org/vep/human/hgvs/3:g.36996633C%3ET/?CADD=1&canonical=1&dbNSFP=phyloP100way_vertebrate,GERP%2B%2B_RS
VEP38_URL = 'https://rest.ensembl.org/vep/human/hgvs/'
VEP37_URL = "https://grch37.rest.ensembl.org/vep/human/hgvs/"
EXT = '/?CADD=1&canonical=1&dbNSFP=phyloP100way_vertebrate,GERP%2B%2B_RS'
GENE_TO_CHROM = {'BRCA1' : 17, 'BRCA2' : 13, 'MSH2': 2, 'MSH6': 2, 'PMS2' : 7, 'MLH1': 3, 'LDLR': 19 , 'APOB': 2, 'PCSK9':1}

def id_variant(gene, n_pos, alt, gene_to_chrom = GENE_TO_CHROM):
    #'17:g.41197701G>A'
    return str(gene_to_chrom[gene]) + ':g.' + str(n_pos) + alt


def request_var_data(variant, vep_url):
    path = './variants/ensemble37/' + variant + '.json'
    if vep_url == VEP38_URL: 
        path = './variants/ensemble38/' + variant + '.json'
    if os.path.exists(path):
        with open(path, 'r') as fp:
            return json.load(fp)
    try:
        api_url = vep_url + variant + EXT
        print(api_url)
        r = requests.get(api_url, headers={ "Content-Type" : "application/json"}, verify=False, timeout=25)
        if not r.ok:
            r.raise_for_status()
            sys.exit()
            return "Bad request"
        
        decoded = r.json()[0]
        with open(path, 'w') as fp:
            json.dump(decoded, fp)
        return decoded
    
    except requests.exceptions.Timeout:
        return "timeout"

