#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 09:27:06 2020

@author: thotran
"""
#'LDLR', 'APOB', 'PCSK9'
import dash_core_components as dcc
import dash_html_components as html

DEFAULT_VARIANTS = {'breast cancer': {'chrom': 13, 'mut_type': 'Insertion', 'gene': 'BRCA2',
                                      'gene_options': [
                                                          {'label': 'BRCA1', 'value': 'BRCA1'},
                                                          {'label': 'BRCA2', 'value': 'BRCA2'}],
                                      'start_pos': 32890639, 'end_pos': 32890640, 'ref': '_', 'alt': 'TTA'}, 
                    'colorectal cancer': {'chrom': 3, 'mut_type': 'Missense', 'gene': 'MLH1',
                                          'gene_options': [
                                                          {'label': 'MSH2', 'value': 'MSH2'},
                                                          {'label': 'MSH6', 'value': 'MSH6'},
                                                          {'label': 'PMS2', 'value': 'PMS2'},
                                                          {'label': 'MLH1', 'value': 'MLH1'}],
                                        'start_pos': 37038124, 'end_pos': 37038124, 'ref': 'C', 'alt': 'T'},
                     'coronary artery disease': {'chrom': 19, 'mut_type': 'Missense', 'gene': 'LDLR',
                                          'gene_options': [
                                                          {'label': 'LDLR', 'value': 'LDLR'},
                                                          {'label': 'APOB', 'value': 'APOB'},
                                                          {'label': 'PCSK9', 'value': 'PCSK9'}],
                                        'start_pos': 11200228, 'end_pos': 11200228, 'ref': 'G', 'alt': 'C'},
                    }

BASE_MENU =  [html.Label('Sex'),
          dcc.Dropdown(id = 'sex', value='F', 
                options = [
                {'label': 'Female', 'value': 'F'},
                {'label': 'Male', 'value': 'M'}],
                style= dict(
                        width='50%',
                    )),
              html.Label('Basic Health Info: Check if you have'),
              dcc.Checklist(
                id= 'obese-hist',
                options = [
                {'label': 'Severe obsesity', 'value': 'obese'},
                {'label': 'Family history', 'value': 'fam_his'}],
                value = ['default'],
                ),
                  ]
#13-32890639-_-TTA
#13-32890631-T-G

def get_mutation_menu(disease):
    vals = DEFAULT_VARIANTS.get(disease)
    return [
        html.Label('Please, input your variant and health information below.'),
              html.Label('Gene'),
              dcc.Dropdown(id = 'gene', value=vals['gene'], 
      options = vals['gene_options'],
      style= dict(
          width='50%'
                )),
        html.Label('Chromosome'),
        dcc.Dropdown(id = 'chrom', value= vals['chrom'], 
          options = [{'label': 1, 'value': 1}, {'label': 2, 'value': 2}, {'label': 3, 'value': 3}, {'label': 7, 'value': 7}, 
                     {'label': 13, 'value': 13}, {'label': 19, 'value': 19}],
          style= dict(
              width='50%',
                    )),
         html.Label('Mutation Type'),
        dcc.Dropdown(id = 'mut_type', value= vals['mut_type'], 
          options = [{'label': 'Insertion', 'value': 'Insertion'}, {'label': 'Nonsense', 'value': 'Nonsense'}, {'label': 'Missense', 'value': 'Missense'}, {'label': 'Silent', 'value': 'Silent'}, {'label': 'Deletion', 'value': 'Deletion'}],
          style= dict(
              width='50%',
                    )),
        html.Label('Nucleotide Position (e.g. 32890631 - 32890631'),

    dcc.Input(id= 'start', value =vals['start_pos'], type = 'number',    
              style= dict(
          width='30%',
                )),
    dcc.Input(id= 'end', value = vals['end_pos'], type = 'number',    
              style= dict(
          width='30%',
                )),
    html.Label('Alteration: Reference --> Alteration (e.g. T-->G, _-->G)'),
    dcc.Input(id= 'ref', value = vals['ref'] , type = 'text', 
              style= dict(
          width='30%',
                )),
    dcc.Input(id= 'alt', value = vals['alt'] , type = 'text', 
              style= dict(
          width='30%',
                )),]



def setup_default_menu(disease):
    return html.Div(get_mutation_menu(disease) + BASE_MENU, style = dict(padding='5%'))

    #elif disease == 'colorectal cancer':
        #return get_mutation_menu(disease) + BASE_MENU

def setup_survival_plot():
    return dcc.Graph(
        id='survival-plot',
        config={
                'modeBarButtonsToRemove': ['autoScale2d', 'select2d', 'zoom2d',
                                           'pan2d', 'toggleSpikelines',
                                           'hoverCompareCartesian',
                                           'zoomOut2d', 'zoomIn2d',
                                           'hoverClosestCartesian',
                                           # 'sendDataToCloud',
                                           'resetScale2d'],
        },)
    
def setup_ph_plot(id):
    return dcc.Graph(
            id='ph-plot-'+id,
            config={
                    'modeBarButtonsToRemove': ['autoScale2d', 'select2d', 'zoom2d',
                                               'pan2d', 'toggleSpikelines',
                                               'hoverCompareCartesian',
                                               'zoomOut2d', 'zoomIn2d',
                                               'hoverClosestCartesian',
                                               # 'sendDataToCloud',
                                               'resetScale2d'],
            })

def setup_covariate_plot(id):
    return  dcc.Graph(
            id='covariate-plot-'+id,
            config={
                    'modeBarButtonsToRemove': ['autoScale2d', 'select2d', 'zoom2d',
                                               'pan2d', 'toggleSpikelines',
                                               'hoverCompareCartesian',
                                               'zoomOut2d', 'zoomIn2d',
                                               'hoverClosestCartesian',
                                               # 'sendDataToCloud',
                                               'resetScale2d'],
                   
            })

def setup_prs_slider(id = 'prs-slider', range_val = (-5,5,0.1)):
    min, max, step = range_val
    return dcc.Slider(
      id = id,
      min= min,
      max= max,
      step = step,
      #marks={i: str(i) for i in range(-5,6)},
      marks={i/2: str(i/2) for i in range(-10,12)},
      value=0,
    )