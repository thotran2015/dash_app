# dash libs
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#app, view, controller  and model modules
from app import app, server
from layouts import layout1, layout2, layout3
import callbacks
from computation import compute_survival

# pydata stack
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
#import requests, sys

# set params
DATABASE_URL = 'postgres://duozofkhzsfjvy:46ef1e44c2b9751801126174b41e124a7f1c847b9e0cf2f27af49a0a3278d5db@ec2-54-235-89-123.compute-1.amazonaws.com:5432/da1e3uq86ab5tu'
conn = create_engine(DATABASE_URL)
server = "https://rest.ensembl.org"


ext = "/vep/human/hgvs/"

reg_ext = "/vep/human/region/"
reg_variant = "1:156084729:156084729:1/A"

#"1:6524705:6524705/T?"
s_variant = '9:g.22125504G>C'
variant = '1:g.156084729G>A'

opt_par ='?CADD=1?'

api_url = server+reg_ext+reg_variant




#1-156084729-G-A
#1-156084750-C-T


###########################
# Data Manipulation / Model
###########################


#########################
# Dashboard Layout / View
#########################

# Set up Dashboard and create layout

app.layout = html.Div(children =[
    html.H1(children = 'Risk Calculator for Coronary Artery Disease, Breast Cancer, or Colorectal Cancer',
             style = {'text-align': 'center'}),
    dcc.Tabs(id="tabs", value='BC', children=[
        dcc.Tab(label='Coronary Artery Disease', value='CAD'),
        dcc.Tab(label='Breast Cancer', value='BC'),
        dcc.Tab(label='Colorectal Cancer', value= 'CC')
    ]), 
    html.Div(id='page-content')
    ])

#############################################
# Interaction Between Components / Controller
#############################################

# Set menu tabs

@app.callback(Output(component_id = 'page-content', component_property = 'children'), 
                [Input(component_id = 'tabs', component_property = 'value')])
def render_tab_title(tab):
    if tab =='CAD':
        return layout1
    elif tab == 'BC':
        return layout2
    elif tab == 'CC':
        return layout3


# start Flask server
if __name__ == '__main__':

    #r = requests.get(api_url, headers={ "Content-Type" : "application/json"})
    # if not r.ok:
    #     r.raise_for_status()
    #     sys.exit()
 
    # decoded = r.json()

    # print('NEXT VARIANT DATA')
    # print('VARIANT_url:' + api_url)
    # print(repr(decoded))

    app.run_server(debug = True)

