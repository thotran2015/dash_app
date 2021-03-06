from dash.dependencies import Input, Output
from app import app
import numpy as np
from callbacks_util import load_model, get_covariate_grps_callback, get_hazard_ratios_callback, get_survival_callback
from process_input import get_pat_data 
from constants import VEP37_URL, COV_DISEASE
import time
#############################################
# Interaction Between Components / Controller
#############################################


COVARIATES = {'log Allele Frequency':np.arange(0, 6, 1), 'Family History': np.arange(0,2), 'Mutations': np.arange(0,2), 
              'PRS': np.arange(0,3), 'sex': np.arange(0,2), 'Regions': np.arange(0,2)}

BRCA2_MODEL_LOC = './models/BRCA2_10_31.pickle'
MLH1_MODEL_LOC = './models/MLH1_model.pickle'
LDLR_MODEL_LOC = './models/LDLR_model.pickle'

#################################################
# TODO: INPUT YOUR FAVORITE SURVIVAL MODEL HERE #
#################################################

MLH1_MODEL = load_model(MLH1_MODEL_LOC)
BRCA2_MODEL = load_model(BRCA2_MODEL_LOC)
LDLR_MODEL = load_model(LDLR_MODEL_LOC)

GENE_MODELS = {'MLH1': MLH1_MODEL, 'BRCA2': BRCA2_MODEL, 'BRCA1': BRCA2_MODEL, 'LDLR': LDLR_MODEL}



#####################################
###### SURVIVAL FUNCTION PLOT #######
#####################################
        
@app.callback(
    #Output('feedback', 'children'),
    Output('loading-output-1', 'children'),
    [Input(component_id='tabs', component_property='value'), 
    Input(component_id='gene', component_property='value'), 
    Input(component_id='mut_type', component_property='value'), 
    Input(component_id='chrom', component_property='value'),
    Input(component_id='start', component_property='value'),
    Input(component_id='end', component_property='value'),
    Input(component_id='ref', component_property='value'),
    Input(component_id='alt', component_property='value'),
    Input(component_id='obese-hist', component_property='value'), 
    Input(component_id='sex', component_property='value')
    ])
def get_feedback(dis_tab, gene, mut_type, chrom, start, end, ref, alt, obese_hist, sex):
    pat_data = get_pat_data(gene, mut_type, chrom, start, end, ref, alt, dis_tab, sex,  obese_hist, VEP37_URL)
    time.sleep(1)
    if len(pat_data) == 0:
        return 'Your variant was not found in the database. Please, enter another variant.'
    else:
        return 'We successfully calculated your result!'
    

@app.callback(
    Output(component_id='survival-plot', component_property='figure'),
    [Input(component_id='tabs', component_property='value'), 
    Input(component_id='gene', component_property='value'), 
    Input(component_id='mut_type', component_property='value'), 
    Input(component_id='chrom', component_property='value'),
    Input(component_id='start', component_property='value'),
    Input(component_id='end', component_property='value'),
    Input(component_id='ref', component_property='value'),
    Input(component_id='alt', component_property='value'),
    Input(component_id='obese-hist', component_property='value'), 
    Input(component_id='sex', component_property='value')
    ])
def plot_survival_function(dis_tab, gene, mut_type, chrom, start, end, ref, alt, obese_hist, sex, prs=0):
    model = GENE_MODELS[gene]
    return get_survival_callback(dis_tab, gene, mut_type, chrom, start, end, ref, alt, obese_hist, sex, prs, model)()




#####################################
###### PARTIAL HARZARD RATIO PLOT ###
#####################################


@app.callback(
    [Output(component_id='ph-plot-0', component_property='figure'), Output(component_id='ph-plot-1', component_property='figure'),
     Output(component_id='ph-plot-2', component_property='figure'), Output(component_id='ph-plot-3', component_property='figure')],
    [Input(component_id='tabs', component_property='value'), 
    Input(component_id='gene', component_property='value'), 
    ])
def plot_ph_ratios(tab, gene):
    model = GENE_MODELS[gene]
    return get_hazard_ratios_callback(gene, model)()
    

#####################################
###### COVARIATE GROUPS PLOT ########
#####################################
    


@app.callback(
    [Output('covariate-plot-' + str(i), 'figure') for i in range(4)], 
    [Input(component_id='tabs', component_property='value'),
    Input(component_id='gene', component_property='value'), 
    Input(component_id='mut_type', component_property='value'), 
    Input(component_id='chrom', component_property='value'),
    Input(component_id='start', component_property='value'),
    Input(component_id='end', component_property='value'),
    Input(component_id='ref', component_property='value'),
    Input(component_id='alt', component_property='value'),
    Input(component_id='obese-hist', component_property='value'), 
    Input(component_id='sex', component_property='value')
      ])
def plot_covariates(dis_tab, gene, mut_type, chrom, start, end, ref, alt, obese_hist, sex, prs=0):
    model = GENE_MODELS[gene]
    data = [get_covariate_grps_callback(cov, COVARIATES[cov], dis_tab, gene, mut_type, chrom, start, end, ref, alt, obese_hist, sex, prs, model)() 
            for cov in COV_DISEASE[dis_tab]]
    return data




