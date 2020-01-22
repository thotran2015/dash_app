#import requests
import pandas as pd
import json
import math
import numpy as np
#from contextlib import closing

#import dropbox
#import csv


###########################
# Data Manipulation / Model
###########################

#to get a user's variant, you need, from the user, the gene, position of the alternation, and actual mutation.
GENES = ['BRCA1', 'BRCA2', 'MSH2', 'MSH6', 'PMS2', 'MLH1', 'LDLR', 'APOB', 'PCSK9']
GENE_TO_CHROM = {'BRCA1' : 17, 'BRCA2' : 13, 'MSH2': 2, 'MSH6': 2, 'PMS2' : 7, 'MLH1': 9, 'LDLR': 19 , 'APOB': 2, 'PCSK9':1}
ACCESS_TOKEN = 'd0gfUKsHc6AAAAAAAAAYRohSgxa_-iaq5sot3YDzsZA1sydQUeJndLwXCW1vbw_8'

# VARIANT_FILE = '/editable_variant_information_condensed.csv'
# PHENOTYPE_FILE = '/partial_phenotype_data.csv'

VARIANT_FILE = './data/variant_info.json'
PHENOTYPE_FILE = './data/phenotypes.json'


BREAST_PAR = [ "PC1", "PC2", "PC3", "PC4", "gps_breastcancer", "fam_hist", "allele_frequency", "Silent", "Nonsense", "Missense", "Deletion", "Frameshift"]
#log allele frequency
COLREC_PAR = [ "PRS", "MSH2", "MSH6" , "MLH1" , "PMS2" , "fam_hist" , "allele_frequency" , "PC1" , "PC2" , "PC3" ,
    "PC4" , "gps_ibd", "Missense" , "Nonsense" , "Frameshift" , "Insertion/Deletion" ]
COR_ARTERY_PAR = []

INPUT_PAR ={'BC': BREAST_PAR, 'CC':COLREC_PAR, 'CAD': COR_ARTERY_PAR }

#parameters to look for in the PHENOTYPE FILE
PHENOTYPE_PAR = {'BC': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_breastcancer'],
                'CC': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_ibd']}


# PHENOTYPE_PAR = {'BC': ['PC1', 'PC2', 'PC3', 'PC4'],
#                 'CC': ['PC1', 'PC2', 'PC3', 'PC4']}

#gene to disease
GENE_TO_DISEASE = {'BC': ['BRCA1', 'BRCA2'], 'CC': ['MSH2', 'MSH6', 'PMS2', 'MLH1'], 'CAD': ['LDLR', 'APOB', 'PCSK9']}

#colorectal cancer variants
#["MSH2 Variant", "MSH6 Variant" , "MLH1 Variant" , "PMS2 Variant"]



#parameters to look for in the VARIANT FILE 
VAR_PAR = ["allele_frequency", "type"]
CONSEQ = ["Silent", "Nonsense", "Missense", "Deletion", "Frameshift", "Insertion/Deletion"]

#links to model coefficients and baseline
BC_MODEL = './data/trained_BC_model.json'
CC_MODEL = './data/trained_CC_model.json'
CAD_MODEL = ''

DISEASE_MODELS = {'BC': BC_MODEL, 'CC': CC_MODEL, 'CAD': CAD_MODEL}

#polygenetic info from the user
#POLYGENETIC_OPTIONS = {'BC': ['fam_hist', 'obese'], 'CC': ['fam_hist', 'obese', 'prs']}
POLYGENETIC_OPTIONS = ['fam_hist', 'obese']
#Average phenotype count (PC) values 

# def access_dropbox_file(file, access_token = ACCESS_TOKEN):
#     dbx = dropbox.Dropbox(access_token)
#     metadata, f = dbx.files_download(file)
#     csv_reader = list(csv.DictReader(f.content.decode().splitlines(), delimiter=','))
#     return pd.DataFrame(csv_reader)

def get_phenotypes(disease='BC', phenotype_file = PHENOTYPE_FILE):
    #df = access_dropbox_file(phenotype_file)
    df = pd.read_json(phenotype_file)
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
    #df = access_dropbox_file(variant_file)
    df = pd.read_json(variant_file)
    df['allele_frequency'] = df['allele_frequency'].fillna(0)
    if var_name in set(df['name']):
        row = df[df['name']==var_name]
        var_args = {conseq: 1 if conseq == row.iloc[0][VAR_PAR[1]] else 0 for conseq in CONSEQ}
        var_args[VAR_PAR[0]]= row.iloc[0][VAR_PAR[0]]
        return var_args
    return 'UNFOUND'
  

# Retrieve Polygenetic Input from user
def get_polygenetic_input(disease, polygenetic_selected, gene_selected, prs=None):
    polygene = {option: 1 if option in polygenetic_selected else 0 for option in POLYGENETIC_OPTIONS}
    if prs !=None:
        polygene["PRS"] = prs

    for gene in GENE_TO_DISEASE[disease]:
        if gene == gene_selected: 
            polygene[gene] = 1
        else:
            polygene[gene] = 0

    return polygene

#Process model input
def process_model_input(var_args, input_args, phenotype_args, disease = 'BC'):
    all_args = {**var_args, **input_args, **phenotype_args}
    if disease == 'BC':
        if 'PRS' in all_args:
            all_args['gps_breastcancer'] = all_args['PRS']
    if disease == 'CC':
        if 'PRS' in all_args:
            all_args['gps_ibd'] = all_args['PRS']

    # all_args['allele_frequency'] = np.log10(float(all_args['allele_frequency']))
    # if all_args['allele_frequency'] == 0:
    #     all_args['allele_frequency'] = 3e-6
    #print('allele:', all_args['allele_frequency'])
    data = [float(all_args[i]) for i in INPUT_PAR[disease]]
    return pd.DataFrame({'data': data})

def process_baseline_coef(disease='BC'):
    disease_model = DISEASE_MODELS[disease]
    df = pd.read_json(disease_model)
    baseline = df["baseline_hazards"].dropna()
    coef = df["coefficients"].dropna()
    return baseline, coef

def get_baseline(disease='BC'):
    baseline, coef = process_baseline_coef(disease)
    return {age: prob for age, prob in baseline.to_dict().items()}

def get_survival_prob(var_args, input_args, phenotype_args, disease='BC'):
    data = process_model_input(var_args, input_args, phenotype_args, disease)
    baseline, coef = process_baseline_coef(disease)
    prod = math.exp(np.sum(coef.to_numpy()*data.to_numpy()))
    return {age: prob*prod for age, prob in baseline.to_dict().items()}



# baseline, coef = process_baseline_coef('BC')
# print(coef*10)

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



# def fetch_data(q, conn):
#     df = pd.read_sql(
#         sql=q,
#         con=conn
#     )
#     return df

# def write_data(df, t, conn):
#     df.to_sql(name = t, con = conn, if_exists= 'append', index = False)


# def get_divisions():
#     '''Returns the list of divisions that are stored in the database'''

#     division_query = (
#         f'''
#         SELECT * FROM datacamp_courses
#         '''
#     )
#     divisions = fetch_data(division_query)
#     divisions = list(divisions['course_name'].sort_values(ascending=True))
#     return divisions

# #print('data from db', get_divisions())


# def write_patients():
#     '''Returns the list of divisions that are stored in the database'''
#     data = { 'course_name': ['hafu'] , 'course_instructor': ['Tho Becky '], 'topic': ['stat']}
#     df = pd.DataFrame(data)
#     if data ['course_name'][0] not in get_divisions():
#         write_data(df, 'datacamp_courses')
#     else:
#         print("Key already existed")
#     #divisions = list(divisions['course_name'].sort_values(ascending=True))
#     #return divisions
# def process_covariates(factor, value):
# 	if factor == 'allele_freq':
# 		return log(value)
# 	else:
# 		return value

# def compute_survival(baseline, coef, data):
# 	return baseline*math.exp(coef*data)
