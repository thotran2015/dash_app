#import requests
import pandas as pd
import json
import math
import numpy as np
#from contextlib import closing

import dropbox
import csv


###########################
# Data Manipulation / Model
###########################

#to get a user's variant, you need, from the user, the gene, position of the alternation, and actual mutation.
GENES = ['BRCA1', 'BRCA2', 'MSH2', 'MSH6', 'PMS2', 'MLH', 'LDLR', 'APOB', 'PCSK9']
GENE_TO_CHROM = {'BRCA1' : 17, 'BRCA2' : 13, 'MSH2': 2, 'MSH6': 2, 'PMS2' : 7, 'MLH1': 9, 'LDLR': 19 , 'APOB': 2, 'PCSK9':1}
ACCESS_TOKEN = 'd0gfUKsHc6AAAAAAAAAYRohSgxa_-iaq5sot3YDzsZA1sydQUeJndLwXCW1vbw_8'

VARIANT_FILE = '/editable_variant_information_condensed.csv'
PHENOTYPE_FILE = '/partial_phenotype_data.csv'


BREAST_PAR = [ "PC1", "PC2", "PC3", "PC4", "gps_breastcancer", "fam_hist", "allele_frequency", "Silent", "Nonsense", "Missense", "Deletion", "Frameshift"]
COLREC_PAR = [ "PRS", "MSH2 Variant", "MSH6 Variant" , "MLH1 Variant" , "PMS2 Variant" , "fam_hist" , "log Allele Frequency" , "PC1" , "PC2" , "PC3" ,
    "PC4" , "GPS IBD", "Missense" , "Nonsense" , "Frameshift" , "Insertion/Deletion" ]
COR_ARTERY_PAR = []

INPUT_PAR ={'BC': BREAST_PAR, 'CC':COLREC_PAR, 'CAD': COR_ARTERY_PAR }

#parameters to look for in the PHENOTYPE FILE
PHENOTYPE_PAR = {'BC': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_breastcancer'],
                'CC': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_ibd']}



#parameters to look for in the VARIANT FILE 
VAR_PAR = ["allele_frequency", "type"]
CONSEQ = ["Silent", "Nonsense", "Missense", "Deletion", "Frameshift"]

#links to model coefficients and baseline
BC_MODEL = 'https://gist.githubusercontent.com/thotran2015/0ade52a9d41353eb52f7a6127736c502/raw/a97126a9710d0dcaed4f2cf1ce3d129d567af723/trained_BC_model.json'
CC_MODEL = 'https://gist.githubusercontent.com/thotran2015/2fb13403e5f38fabe10baa16998d1b52/raw/9c864e50a9db81832f20086d18c689f0797ce3c5/trained_CC_model.json'

#polygenetic info from the user
#POLYGENETIC_OPTIONS = {'BC': ['fam_hist', 'obese'], 'CC': ['fam_hist', 'obese', 'prs']}
POLYGENETIC_OPTIONS = ['fam_hist', 'obese']
#Average phenotype count (PC) values 

def access_dropbox_file(file, access_token = ACCESS_TOKEN):
    dbx = dropbox.Dropbox(access_token)
    metadata, f = dbx.files_download(file)
    csv_reader = list(csv.DictReader(f.content.decode().splitlines(), delimiter=','))
    return pd.DataFrame(csv_reader)

def get_phenotypes(disease='BC', phenotype_file = PHENOTYPE_FILE):
    df = access_dropbox_file(phenotype_file)
    if disease in PHENOTYPE_PAR:
        print(df[PHENOTYPE_PAR[disease]].apply(pd.to_numeric).mean())
        return df[PHENOTYPE_PAR[disease]].apply(pd.to_numeric).mean(axis = 0, skipna = True)
    else:
        return 'No Data in Phenotype File'


def id_variant(gene, n_pos, alt, gene_to_chrom = GENE_TO_CHROM):
	return str(gene_to_chrom[gene]) + '-' + str(n_pos) + '-' + alt

# Obtain Variant Info
def get_variant_data(var_name, disease='BC', variant_file = VARIANT_FILE):
    #var_name = id_variant(gene, n_pos, alt)
    df = access_dropbox_file(variant_file)
    if var_name in set(df['name']):
        row = df[df['name']==var_name]
        var_args = {conseq: 1 if conseq == row.iloc[0][VAR_PAR[1]] else 0 for conseq in CONSEQ}
        var_args[VAR_PAR[0]]= row.iloc[0][VAR_PAR[0]]
        return var_args
    return 'no variant in database'


    # dbx = dropbox.Dropbox(access_token)
    # metadata, f = dbx.files_download(variant_file)
    # csv_reader = list(csv.DictReader(f.content.decode().splitlines(), delimiter=','))
    # df = pd.DataFrame(csv_reader)

    

# Retrieve Polygenetic Input
def get_polygenetic_input(polygenetic_selected, prs=None):
    polygene = {option: 1 if option in polygenetic_selected else 0 for option in POLYGENETIC_OPTIONS}
    if prs !=None:
        polygene['prs'] = prs
    return polygene

#Process model input
def process_model_input(var_args, input_args, phenotype_args, disease = 'BC'):
    all_args = {**var_args, **input_args, **phenotype_args}
    data = [float(all_args[i]) for i in INPUT_PAR[disease]]
    return pd.DataFrame({'data': data})

def process_baseline_coef(df):
    baseline = df.head(-12).dropna(axis = 1)
    coef = df.tail(12).dropna(axis = 1)
    return baseline, coef

def survival_rate(var_args, input_args, phenotype_args, disease= BC_MODEL):
    data = process_model_input(var_args, input_args, phenotype_args)
    baseline, coef = process_baseline_coef(pd.read_json(disease))
    print('input data & coeff: ', data, coef.to_numpy())
    print('prod of coef and data: ', coef.to_numpy()*data)
    prod = math.exp(np.sum(coef.to_numpy()*data))
    return {age: baseline['baseline_hazards'][age]*prod for age in baseline.index}, {age: baseline['baseline_hazards'][age] for age in baseline.index}

# dbx = dropbox.Dropbox(ACCESS_TOKEN)
# metadata, f = dbx.files_download(DROPBOX_FILE)
# csv_reader = list(csv.DictReader(f.content.decode().splitlines(), delimiter=','))
# df = pd.DataFrame(csv_reader)
# row = df[df['name']=='1-156084729-G-A']
# var_args = {conseq: 1 if conseq == row.iloc[0][VAR_PAR[1]] else 0 for conseq in CONSEQ}
# var_args[VAR_PAR[0]]= float(row.iloc[0][VAR_PAR[0]])

# print(var_args)

###########################
# SQL read and write
###########################



def fetch_data(q, conn):
    df = pd.read_sql(
        sql=q,
        con=conn
    )
    return df

def write_data(df, t, conn):
    df.to_sql(name = t, con = conn, if_exists= 'append', index = False)


def get_divisions():
    '''Returns the list of divisions that are stored in the database'''

    division_query = (
        f'''
        SELECT * FROM datacamp_courses
        '''
    )
    divisions = fetch_data(division_query)
    divisions = list(divisions['course_name'].sort_values(ascending=True))
    return divisions

#print('data from db', get_divisions())


def write_patients():
    '''Returns the list of divisions that are stored in the database'''
    data = { 'course_name': ['hafu'] , 'course_instructor': ['Tho Becky '], 'topic': ['stat']}
    df = pd.DataFrame(data)
    if data ['course_name'][0] not in get_divisions():
        write_data(df, 'datacamp_courses')
    else:
        print("Key already existed")
    #divisions = list(divisions['course_name'].sort_values(ascending=True))
    #return divisions
def process_covariates(factor, value):
	if factor == 'allele_freq':
		return log(value)
	else:
		return value

def compute_survival(baseline, coef, data):
	return baseline*math.exp(coef*data)
