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
#GENE_TO_str(chrom) = {'BRCA1' : 17, 'BRCA2' : 13, 'MSH2': 2, 'MSH6': 2, 'PMS2' : 7, 'MLH1': 3, 'LDLR': 19 , 'APOB': 2, 'PCSK9':1}

#def id_variant(gene, n_pos, str(alt), gene_to_str(chrom) = GENE_TO_str(chrom)):
    #'17:g.41197701G>A'
    #return str(gene_to_str(chrom)[gene]) + ':g.' + str(n_pos) + str(alt)


def id_variant(mut_type, chrom, start, end, ref, alt):
    if mut_type == 'Insertion':
        return str(chrom) + ':g.' + str(start) + '_'+ str(end)+ 'ins' + str(alt)
    elif mut_type == 'Deletion':
        return str(chrom) + ':g.' + str(start) + '_'+ str(end)+ 'del'
    elif mut_type == 'Insertion/Deletion': 
        return str(chrom) + ':g.' + str(start) + '_'+ str(end)+ 'delins' + str(ref)
    elif mut_type == 'Duplication':
        return str(chrom) + ':g.' + str(start) + '_' + str(end)+ 'dup'
    elif mut_type == 'Frameshift' or mut_type == 'Unknown' or mut_type =='Stop codon mutation':
        if str(ref) == '_':
            return str(chrom) + ':g.' + str(start) + '_'+ str(end)+ 'ins' + str(alt)
        if str(alt) == '_':
            return str(chrom) + ':g.' + str(start) + '_'+ str(end)+ 'del' + str(ref)
    elif mut_type =='Nonsense':
        if str(ref) == '_':
            return str(chrom) + ':g.' + str(start) + '_'+ str(end)+ 'ins' + str(alt)
        elif str(alt) == '_':
            return str(chrom) + ':g.' + str(start) + '_'+ str(end)+ 'del' + str(ref)
        else:
            return str(chrom) + ':g.' + str(start) + str(ref) + '>' + str(alt)
    else:
        return str(chrom) + ':g.' + str(start) + str(ref) + '>' + str(alt)


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

