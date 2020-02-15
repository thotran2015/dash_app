
import pandas as pd
import numpy as np
from load_model import get_patient_profiles, fit_lifelines_model, get_covariate_groups, load_model, get_partial_hazard_ratio
import plotly.graph_objs as go


###########################
# Data Manipulation / Model
###########################

#to get a user's variant, you need, from the user, the gene, position of the alternation, and actual mutation.
GENES = ['BRCA1', 'BRCA2', 'MSH2', 'MSH6', 'PMS2', 'MLH1', 'LDLR', 'APOB', 'PCSK9']
GENE_TO_CHROM = {'BRCA1' : 17, 'BRCA2' : 13, 'MSH2': 2, 'MSH6': 2, 'PMS2' : 7, 'MLH1': 9, 'LDLR': 19 , 'APOB': 2, 'PCSK9':1}
ACCESS_TOKEN = 'd0gfUKsHc6AAAAAAAAAYRohSgxa_-iaq5sot3YDzsZA1sydQUeJndLwXCW1vbw_8'

VARIANT_FILE = './data/variant_info.json'
PHENOTYPE_FILE = './data/phenotypes.json'



coeff_names = {"gps_breastcancer": 'GPS',  }

BREAST_PAR = [ "PC1", "PC2", "PC3", "PC4", "gps_breastcancer", "fam_hist", "allele_frequency", "Silent", "Nonsense", "Missense", "Deletion", "Frameshift"]
#log allele frequency
COLREC_PAR = [ "PRS", "MSH2", "MSH6" , "MLH1" , "PMS2" , "fam_hist" , "allele_frequency" , "PC1" , "PC2" , "PC3" ,
    "PC4" , "gps_ibd", "Missense" , "Nonsense" , "Frameshift" , "Insertion/Deletion" ]
COR_ARTERY_PAR = []

INPUT_PAR ={'BC': BREAST_PAR, 'CC':COLREC_PAR, 'CAD': COR_ARTERY_PAR }

#parameters to look for in the PHENOTYPE FILE
PHENOTYPE_PAR = {'BC': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_breastcancer'],
                'CC': ['PC1', 'PC2', 'PC3', 'PC4', 'gps_ibd']}



#gene to disease
GENE_TO_DISEASE = {'BC': ['BRCA1', 'BRCA2'], 'CC': ['MSH2', 'MSH6', 'PMS2', 'MLH1'], 'CAD': ['LDLR', 'APOB', 'PCSK9']}

#colorectal cancer variants
#["MSH2 Variant", "MSH6 Variant" , "MLH1 Variant" , "PMS2 Variant"]

DISEASES = {'BC': 'Breast Cancer', 'CC': 'Colorectal Cancer', 'CAD': 'Coronary Artery Disease'}



#parameters to look for in the VARIANT FILE 
VAR_PAR = ["allele_frequency", "type"]
CONSEQ = ["Silent", "Nonsense", "Missense", "Deletion", "Frameshift", "Insertion/Deletion"]

#links to model coefficients and baseline
BC_MODEL = './data/trained_BC_model.json'
CC_MODEL = './data/trained_CC_model.json'
CAD_MODEL = ''

DISEASE_MODELS = {'BC': BC_MODEL, 'CC': CC_MODEL, 'CAD': CAD_MODEL}

POLYGENETIC_OPTIONS = ['fam_hist', 'obese']


# DATA = get_patient_profiles('./data/patient_profiles.csv')
# #MODEL = load_model()
# MODEL = fit_lifelines_model(DATA)

 #print(MODEL.summary.index)
#model_loc = './models/BRCA2_10_31.pickle'
#load_model(model_loc)
def get_phenotypes(disease='BC', phenotype_file = PHENOTYPE_FILE):
    #df = access_dropbox_file(phenotype_file)
    df = pd.read_json(phenotype_file)
    if disease in PHENOTYPE_PAR:
        return df[PHENOTYPE_PAR[disease]].apply(pd.to_numeric).mean(axis = 0, skipna = True)
    else:
        return 'No Data in Phenotype File'


def id_variant(gene, n_pos, alt, gene_to_chrom = GENE_TO_CHROM):
    #'17:g.41197701G>A'
    #return str(gene_to_chrom[gene]) + ':g.' + str(n_pos) + alt
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
    all_args['allele_frequency'] = -np.log10(float(all_args['allele_frequency']))
    if all_args['allele_frequency'] == 0.0:
        all_args['allele_frequency'] = 3e-6
    data = [float(all_args[i]) for i in INPUT_PAR[disease]]
    df = pd.DataFrame({'patient': data})
    labels = ["PC1", "PC2", "PC3", "PC4", "GPS", "Family History", "log Allele Frequency", "Silent", "Nonsense", "Missense", "Insertion/Deletion", "Frameshift"]
    df['labels'] = labels
    df = df.set_index('labels').T
    df['GERP'] = -5
    df['PRS'] = all_args['PRS']
    df['Missense']=df['Silent']
    return df.drop(columns = ['Silent'])


def process_baseline_coef(disease='BC'):
    disease_model = DISEASE_MODELS[disease]
    df = pd.read_json(disease_model)
    #baseline = df["baseline_hazards"].dropna()
    coef = df["coefficients"].dropna()
    model = load_model()
    baseline = model.baseline_survival_
    return baseline['baseline survival'] , coef

def get_baseline(disease='BC'):
    baseline, coef = process_baseline_coef(disease)
    return {age: prob for age, prob in baseline.to_dict().items()}

def get_survival_prob(var_args, input_args, phenotype_args, disease='BC'):
    data = process_model_input(var_args, input_args, phenotype_args, disease)
    baseline, coef = process_baseline_coef(disease)
    model = load_model()
    return model.predict_survival_function(data)['patient'].to_dict()

def fill_survival_func(tab, baseline, survival_score = None):
    data = [
    {'x': list(baseline.keys()), 'y': list(baseline.values()), 'type': 'line', 'name': 'baseline', 'marker': dict(color='rgb(55, 83, 109)') },
            ]
    if survival_score!= None:
        data.append(
            {'x': list(survival_score.keys()), 'y': list(survival_score.values()), 'type': 'line', 'name': 'individual', 'marker': dict(color='rgb(26, 118, 255)') }
                )
    return {
        'data': data,
        'layout': {
                'title': 'Survival Probability of '+ DISEASES[tab],
                'xaxis': {
                    'title': 'Age',
                    'type': 'linear' 
                },
                'yaxis' : {
                    'title': 'Survival Probability',
                    'type': 'linear' 
                },
            },}
    
def get_plot_layout(title, xlabel, ylabel):
    return { 
            'title' : title,
            'xaxis': {
                'title': xlabel,
                'type': 'linear' 
                },
            'yaxis' : {
                'title': ylabel,
                'type': 'linear' 
                },
            }


  
def get_callback(cov, val_range, m = MODEL, get_cov_weights = get_covariate_groups):
    covariate= cov
    if cov =='type':
        covariate= ['Missense', 'Nonsense', 'Frameshift', 'Insertion/Deletion', 'Other']
    covariate_groups = get_cov_weights(m, covariate, val_range= val_range)
    def fill_covariate_groups(cov_data, layout):
        return {'data': cov_data,
                'layout': layout
                }  
    def plot_covariate_groups():
        cov_data = [
             {'x': xy[0], 'y': xy[1], 'type': 'line', 'name': label, }
             for i, (label, xy) in enumerate(covariate_groups.items())
             ]
        layout = get_plot_layout('Survival based on '+ cov, 'Age', 'HR')
        return fill_covariate_groups(cov_data,layout)
    return plot_covariate_groups




def get_ph_ratios_callback(model= MODEL, get_partial_hazard_ratio = get_partial_hazard_ratio):
    ph_ratios = get_partial_hazard_ratio(model)
    def fill_ph_ratios_plot(ph_data):
        return {'data': ph_data,
                 'layout': { 
                     'title' : 'Partial Hazard Ratio ',
                     'xaxis': {
                         'title': 'HR',
                         'type': 'linear' 
        
                         },
                     'yaxis' : {
                         'type': 'category' 
        
                         },
                     }} 

    def plot_box_plot_coef(covs = ['PRS', 'CADD', 'log Allele Frequency']):
        ph_data = [
          {'x': xy, 'y': [i]*len(xy), 'type': 'scatter', 'name': i, 'mode':'lines+markers',
              } for i, xy in ph_ratios.items() if i in covs
          ]
        ph_data1 = [
          {'x': xy, 'y': [i]*len(xy), 'type': 'scatter', 'name': i, 'mode':'lines+markers',
              } for i, xy in ph_ratios.items() if i in ['Missense', 'Nonsense', 'Frameshift', 'Insertion/Deletion']
          ]
        return fill_ph_ratios_plot(ph_data), fill_ph_ratios_plot(ph_data1)
    return plot_box_plot_coef
    
    
# def get_ph_ratios_error_callback(model= MODEL):
#     def plot_box_plot_coef():
#         ph_ratios = get_partial_hazard_ratio(model)
#         print(ph_ratios)
#         ph_data = [
#           {'x': xy, 'y': [i]*len(xy), 'type': 'scatter', 'name': i, 'mode':'lines+markers',
#               } for i, xy in ph_ratios.items()
#           ]
#         # for i, xy in ph_ratios.items():
#         #     ph_data.append({'x': [xy[1]], 'y': [i], 'type': 'scatter', 'name': i, 'mode':'markers', 
#         #                     'marker': {'size': 10
#         #                         },
#         #       } )
            
        
#         return fill_ph_ratios_plot(ph_data)
#     return plot_box_plot_coef

#print(MODEL.hazard_ratios_)
#get_partial_hazard_ratio(MODEL)
# baseline, coef = process_baseline_coef('BC')
# print(coef*10)


# def access_dropbox_file(file, access_token = ACCESS_TOKEN):
#     dbx = dropbox.Dropbox(access_token)
#     metadata, f = dbx.files_download(file)
#     csv_reader = list(csv.DictReader(f.content.decode().splitlines(), delimiter=','))
#     return pd.DataFrame(csv_reader)

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
