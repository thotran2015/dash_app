#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 09:27:06 2020

@author: thotran
"""

import dash_core_components as dcc
import dash_html_components as html


def setup_polygenetic_checklist(id):
    return html.Div(
      #style={'width':'10%', 'height':'100%','float':'left'},
      children = [
          dcc.Checklist(
            id= id,
            options = [
            {'label': 'Severe obsesity', 'value': 'obese'},
            {'label': 'Family history', 'value': 'fam_his'}],
            value = ['default'],
            labelStyle = {'display': 'block'}),
      ])
def setup_covariate_plot(id):
    return html.Div( 
            dcc.Graph(
            id='covariate-plot-'+id,
            config={
                    'modeBarButtonsToRemove': ['autoScale2d', 'select2d', 'zoom2d',
                                               'pan2d', 'toggleSpikelines',
                                               'hoverCompareCartesian',
                                               'zoomOut2d', 'zoomIn2d',
                                               'hoverClosestCartesian',
                                               # 'sendDataToCloud',
                                               'resetScale2d']
            }), 
            style = {'width': '50%', 'display': 'inline-block' }
            )
def setup_survival_plot(id):
    return dcc.Graph(
        id='survival-plot-'+id,
        config={
                'modeBarButtonsToRemove': ['autoScale2d', 'select2d', 'zoom2d',
                                           'pan2d', 'toggleSpikelines',
                                           'hoverCompareCartesian',
                                           'zoomOut2d', 'zoomIn2d',
                                           'hoverClosestCartesian',
                                           # 'sendDataToCloud',
                                           'resetScale2d']
        })
    
def setup_ph_plot(id):
    return html.Div( 
            dcc.Graph(
            id='ph-plot-'+id,
            config={
                    'modeBarButtonsToRemove': ['autoScale2d', 'select2d', 'zoom2d',
                                               'pan2d', 'toggleSpikelines',
                                               'hoverCompareCartesian',
                                               'zoomOut2d', 'zoomIn2d',
                                               'hoverClosestCartesian',
                                               # 'sendDataToCloud',
                                               'resetScale2d']
            }), 
            style = {'width': '50%', 'display': 'inline-block' }
            )

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