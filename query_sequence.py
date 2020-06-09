#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 11:20:43 2020

@author: thotran
"""
import os
import json
import requests, sys

SEQ37_URL = "https://grch37.rest.ensembl.org/sequence/region/human/"
SEQ38_URL = 'https://rest.ensembl.org/sequence/region/human/'
EXT = '?'

def request_sequence_data(region, seq_url):
    path = './sequences/ensemble37/' + region + '.json'
    if seq_url == SEQ38_URL: 
        path = './sequences/ensemble38/' + region + '.json'
    if os.path.exists(path):
        with open(path, 'r') as fp:
            return json.load(fp)
    try:
        api_url = seq_url + region + EXT
        print(api_url)
        r = requests.get(api_url, headers={ "Content-Type" : "application/json"}, verify=False, timeout=25)
        if not r.ok:
            return "Bad request"
            #r.raise_for_status()
            #sys.exit()
            #return "Bad request"
        decoded = r.json()
        with open(path, 'w') as fp:
            json.dump(decoded, fp)
        return decoded
    except requests.exceptions.Timeout:
        return "timeout"


def id_region(n_pos):
    return 'X:'+ str(n_pos-1) +'..'+ str(n_pos+1) +':1'

def get_CpG(n_pos, seq_url):
    reg = id_region(n_pos)
    data = request_sequence_data(reg, seq_url)
    seq = data['seq']
    if 'CG' in seq:
        return {'CpG Affecting': 1, 'Non CpG Affecting': 0}
    else:
        return {'CpG Affecting': 0, 'Non CpG Affecting': 1}

