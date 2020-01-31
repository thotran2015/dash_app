#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 17:01:25 2020

@author: thotran
"""
import requests, sys
VEP_SERVER = "https://grch37.rest.ensembl.org/"
EXT = "/vep/human/hgvs/"


def request_var_data(variant):
    #vep_server = "https://rest.ensembl.org"
    # vep_server = "https://grch37.rest.ensembl.org/"
    # ext = "/vep/human/hgvs/"
    # reg_ext = "/vep/human/region/"
    # ##reg_variant = "1:156084729:156084729:1/A"
    # ##
    # ###"1:6524705:6524705/T?"
    # #s_variant = '9:g.22125504G>C'
    # #variant = '1:g.156084756C>T'
    # reg_variant = "1:156084756:156084756:1/A"
    #'1:g.156084729G>A'
    ##AGT:c.803T>C
    ##opt_par ='?CADD=1?'
    api_url = VEP_SERVER + EXT + variant +'?CADD=1&Conservation=1'
    #api_url_ext = vep_server + reg_ext + reg_variant
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
    
    
def collect_transcript_conseq(consequences):
    for conseq in consequences:
        return conseq
    