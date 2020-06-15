#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 10:22:23 2020

@author: thotran
"""
import requests, sys
import json
import os 
from constants import VEP38_URL, EXT
from store_data import set_redis, get_redis

#https://rest.ensembl.org/vep/human/hgvs/3:g.36996633C%3ET/?CADD=1&canonical=1&dbNSFP=phyloP100way_vertebrate,GERP%2B%2B_RS




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
    if get_redis(variant):
        print('geting variant')
        return get_redis(variant)
    try:
        api_url = vep_url + variant + EXT
        print(api_url)
        r = requests.get(api_url, headers={ "Content-Type" : "application/json"}, verify=False, timeout=25)
        if not r.ok:
            return "Bad request"
            #r.raise_for_status()
            #sys.exit()
            #return "Bad request"
        decoded = r.json()[0]
        print('saving data in redis')
        set_redis(variant, json.dumps(decoded))
        with open(path, 'w') as fp:
            print('saving data in filesystem')
            json.dump(decoded, fp)
        return decoded
    except requests.exceptions.Timeout:
        return "timeout"

