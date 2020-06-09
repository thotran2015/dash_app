# dash libs
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#app, view, controller  and model modules
from app import app, server
from layouts import layout1, layout2, layout3
import callbacks
import process_input as pi


VEP37_URL = "https://grch37.rest.ensembl.org/vep/human/hgvs/"

###########################
# Data Manipulation / Model
###########################


#########################
# Dashboard Layout / View
#########################

# Set up Dashboard and create layout

# app.layout = html.Div(
#     id = 'header', className = 'row',
#     children =[ html.H1(children = 'Risk Calculator for Coronary Artery Disease, Breast Cancer, or Colorectal Cancer',
#              style = {'text-align': 'center'}),
    
#     dcc.Tabs(id="tabs", value='BC', children=[
#         dcc.Tab(label='Coronary Artery Disease', value='CAD'),
#         dcc.Tab(label='Breast Cancer', value='BC'),
#         dcc.Tab(label='Colorectal Cancer', value= 'CC')
#     ]), 
#     html.Div(id='page-content')
#     ])


app.layout = html.Div(children = [
    html.Div(html.H1('Risk Calculator for Coronary Artery Disease, Breast Cancer, or Colorectal Cancer'),
             style = {'text-align': 'center', 'padding': '1%'}, id = 'header', className = 'row'),
    html.Div(    
        dcc.Tabs(id="tabs", value='CAD', 
        children=[
        dcc.Tab(label='Coronary Artery Disease', value='CAD'),
        dcc.Tab(label='Breast Cancer', value='BC'),
        dcc.Tab(label='Colorectal Cancer', value= 'CC')
        ]), style = dict(padding = '2%'), id = 'disease-page', className = 'row' ),
        html.Div(id='page-content',  style = dict(padding = '2%', backgroundColor = 'lightgrey')),
        ])

#############################################
# Interaction Between Components / Controller
#############################################
  # Set menu tabs

# @app.callback(Output(component_id = 'page-content', component_property = 'children'), 
#                  [Input(component_id='tabs', component_property='value'),
#     Input(component_id='gene', component_property='value'), 
#     Input(component_id='mut_type', component_property='value'), 
#     Input(component_id='chrom', component_property='value'),
#     Input(component_id='start', component_property='value'),
#     Input(component_id='end', component_property='value'),
#     Input(component_id='ref', component_property='value'),
#     Input(component_id='alt', component_property='value'),
#     Input(component_id='obese-hist', component_property='value'), 
#     Input(component_id='sex', component_property='value')])
# def render_content(disease, gene, mut_type, chrom, start, end, ref, alt, obese_hist, sex):
#     data = pi.get_pat_data(gene, mut_type, chrom, start, end, ref, alt, disease, sex, obese_hist, VEP37_URL)
#     if len(data) == 0:
#         return 'No result'
        
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
    app.run_server(debug = True)

