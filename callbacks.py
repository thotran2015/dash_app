from dash.dependencies import Input, Output
from app import app
import computation as model


# import requests
# import pandas as pd
# import json
# import ndjson
# import math
# import numpy as np

#############################################
# Interaction Between Components / Controller
#############################################

#generate tab
DISEASES = {'BC': 'Breast Cancer', 'CC': 'Colorectal Cancer', 'CAD': 'Coronary Artery Disease'}

@app.callback(
    Output('prs', 'children'),
    [Input('prs-slider', 'value')])
def update_output(value):
    return 'You have selected PRS of {}'.format(value)

# @app.callback(
#     Output(component_id='test-output', component_property='children'),
#     [Input(component_id='tabs', component_property='value'), 
#     Input(component_id='gene', component_property='value'), Input(component_id='n_pos', component_property='value'), Input(component_id='alt', component_property='value'),
#     Input(component_id='obese-hist', component_property='value'), Input(component_id='prs-slider', component_property='value')
#     ])
# def get_checklists(tab, gene, n_pos, alt, obese_hist, prs):
#     phenotype_args = model.get_phenotypes(disease = tab)
#     variant = model.id_variant(gene, n_pos, alt)
#     var_args = model.get_variant_data(variant)
#     #var_args = model.get_variant_data(gene, n_pos, alt, disease = tab) 
#     input_args = model.get_polygenetic_input(tab, obese_hist, gene, prs)

#     #survival_score = model.survival_rate(var_args, input_args, phenotype_args)
#     return list(input_args.values())




@app.callback(
    Output(component_id='survival-plot', component_property='figure'),
    [Input(component_id='tabs', component_property='value'), 
    Input(component_id='gene', component_property='value'), Input(component_id='n_pos', component_property='value'), Input(component_id='alt', component_property='value'),
    Input(component_id='obese-hist', component_property='value'), Input(component_id='prs-slider', component_property='value')
    ])
def get_checklists(tab, gene, n_pos, alt, obese_hist, prs):
    if tab == "CAD":
        return {}
    phenotype_args = model.get_phenotypes(disease = tab)
    variant = model.id_variant(gene, n_pos, alt)
    var_args = model.get_variant_data(variant, disease= tab)
    baseline = model.get_baseline(disease= tab)
    if var_args == 'UNFOUND':
        return {
        'data': [
                {'x': list(baseline.keys()), 'y': list(baseline.values()), 'type': 'line', 'name': 'baseline', 'marker': dict(color='rgb(55, 83, 109)') },

            ],
        'layout': {
                'title': 'Baseline Survival Probability of '+ DISEASES[tab]
            }
        }
    else:
        #input_args = model.get_polygenetic_input(obese_hist, prs)
        input_args = model.get_polygenetic_input(tab, obese_hist, gene, prs)
        survival_score = model.get_survival_prob(var_args, input_args, phenotype_args, disease = tab)
        return {
            'data': [
                    {'x': list(baseline.keys()), 'y': list(baseline.values()), 'type': 'line', 'name': 'baseline', 'marker': dict(color='rgb(55, 83, 109)') },

                    {'x': list(survival_score.keys()), 'y': list(survival_score.values()), 'type': 'line', 'name': 'individual', 'marker': dict(color='rgb(26, 118, 255)') },
                ],
            'layout': { 
                'title' : 'Survival Probability of ' + DISEASES[tab],
                'xaxis': {
                    'title': 'Survival Probability',
                    'type': 'linear' 
                    },
                'yaxis' : {
                    'title': 'Survival Probability',
                    'type': 'linear' 
                    },
            }
            }
    


# @app.callback(Output(component_id = 'disease', component_property = 'options'),
#               [Input(component_id = 'tabs', component_property = 'value')])
# def render_tab_content(tab):
#     if tab == 'CAD':
#         return [
#                 {'label': 'Coronary Artery Disease', 'value': 'CAD'},
#                 {'label': 'Breast Cancer', 'value': 'BC'},
#                 {'label': 'Colorectal Cancer', 'value': 'CC'}
#                     ]
#     elif tab == 'BC':
#         return [
#                 {'label': 'Coronary Artery Disease', 'value': 'CAD'},
#                 {'label': 'Breast Cancer', 'value': 'BC'},
#                 {'label': 'Colorectal Cancer', 'value': 'CC'}
#                     ]
#     elif tab == 'CC':
#         return [
#                 {'label': 'Coronary Artery Disease', 'value': 'CAD'},
#                 {'label': 'Breast Cancer', 'value': 'BC'},
#                 {'label': 'Colorectal Cancer', 'value': 'CC'}
#  


# #collect breast cancer data
# @app.callback(Output(component_id = '', component_property = ''),
#               [Input(component_id = 'PRS', component_property = 'value'), Input(component_id = '', component_property = '')])
# def update_value(tab):
#     return 

#coef_baseline= pd.read_json('./sample_data.json')
#data = pd.DataFrame({'data': [0, 1,2,3,4,5, 6, 7, 8, 9, 10, 0]})

#wrap a callback function using decorator. callback is func that gets called once the user input submit some info

# @app.callback(
#     Output(component_id='survival-plot', component_property='figure'),
#     [Input(component_id='gene', component_property='value'), Input(component_id='n_pos', component_property='value'), Input(component_id='alt', component_property='value'),
#     Input(component_id='obese-hist', component_property='value'), Input(component_id='prs', component_property='value')
#     ])
# def get_checklists(obese_hist, prs):
#     pcs = model.get_PCs()
#     var_args = model.get_variant_data(gene, n_pos, alt, access_token) 
#     input_args = model.get_polygenetic_input(obese_hist, prs)

#     survival_score = model.survival_rate(var_args, input_args)
#     return {
#          'data': [
#                  {'x': list(survival_score.keys()), 'y': list(survival_score.values()), 'type': 'line', 'name': 'SF'},
#              ],
#          'layout': {
#                  'title': 'Survival Probability of Coronary Artery Disease' 
#              }
#          }



# @app.callback(
#     Output(component_id='survival-plot', component_property='figure'),
#     [
#     Input(component_id='gene', component_property='value'), Input(component_id='n_pos', component_property='value'), Input(component_id='alt', component_property='value'),
#     Input(component_id='obese-hist', component_property='options'), Input(component_id='prs', component_property='value')
#     ])
# def update_outcome(gene, n_pos, alt, obese_hist ,prs):
#     var_args = get_variant_data(gene, n_pos, alt)
#     input_args = get_polygenetic_input(fam_hist, prs, severe_obsese)
#     survival_score = model.survival_rate(var_args, input_args)
#     return {
#         'data': [
#                 {'x': list(survival_score.keys()), 'y': list(survival_score.values()), 'type': 'line', 'name': 'SF'},
#             ],
#         'layout': {
#                 'title': 'Survival Probability of Coronary Artery Disease' 
#             }
#         }




#update graph for breast cancer
# @app.callback(
#     Output(component_id='survival-plot', component_property='figure'),
#     [
#     Input(component_id='pc1', component_property='value'), Input(component_id='pc2', component_property='value'),
#     Input(component_id='pc3', component_property='value'), Input(component_id='gps', component_property='value'),
#     Input(component_id='al-freq', component_property='value'), 
#     Input(component_id='basic-health-info', component_property='value'),
#     Input(component_id='genetic-info', component_property='value')
#     ])
# def update_outcome(pc1, pc2, pc3, gps, al_freq,basic_health_info, genetic_info):
#     # "pc1" : 0.00968356984803728,
# #      "pc2" : 0.0028658086344917192,
# #      "pc3" : 0.06838126030467456,
# #      "pc4" : 0.0035710759997293977,
# #      "gps_bc" : 0.1264046323370161,
# #      "family_history" : 0.5579534577158256,
# #      "allele_frequency" : 0.4134539088816637,
# #      "Silent" : -0.37973637436929514,
# #      "Nonsense" : 0.9416360821766052,
# #      "Missense" : -0.42804138284983706,
# #      "Deletion" : 0.6590958454872645,
# #      "Frameshift" : 1.0398951370002338
#     data_list= [pc1, pc2, pc3, gps, 0, al_freq, 1, 0, 0, 0, 0, 0]
#     input_data = model.process_input(data_list)
#     survival_score = model.survival_rate(model.coef_baseline, input_data)
#     return {
#         'data': [
#                 {'x': list(survival_score.keys()), 'y': list(survival_score.values()), 'type': 'line', 'name': 'SF'},
#             ],
#         'layout': {
#                 'title': 'Survival Probability of Coronary Artery Disease' 
#             }
#         }
    

#update tab for each disease
# @app.callback(
#     Output(component_id='tab_label', component_property='children'),
#     [Input(component_id='tabs', component_property='value')]
#     )
# def update_graph(tab):
#     prompt = 'Input Data About '
#     if tab == 'CAD':
#         return prompt + 'Coronary Artery Disease'
#     elif tab == 'BC':
#         return prompt + 'Breast Cancer'
#     elif tab == 'CC':
#         return prompt + 'Coronary Cancer'


# coef_baseline= pd.read_json('./sample_data.json')
# data = pd.DataFrame({'data': [0, 1,2,3,4,5, 6, 7, 8, 9, 10, 0]})
# def process_data(df):
#     baseline = df.head(-12).dropna(axis = 1)
#     coef = df.tail(12).dropna(axis = 1)
#     return baseline, coef

# def survival_rate(coef_baseline, data):
#     baseline, coef = process_data(coef_baseline)
#     prod = math.exp(np.sum(coef.to_numpy()*data))
#     return {age: baseline['baseline_hazards'][age] for age in baseline.index}

# import requests
# import pandas as pd
# import json
# import ndjson

# url = "http://acmg59api.ngrok.io/api/example"
# json_content = requests.get(url).json()
# content = json.dumps(json_content)
# df = pd.read_json(content)
# coef = df.tail(12)
# baseline = df.head(-12)

# def process_covariates():
#     #a_freq = math.log(af)
#     return 'Hello'
    
    

# def hazard_func(covariates, baseline = BASELINE, coef = COEF):
#     return baseline*coef*covariates