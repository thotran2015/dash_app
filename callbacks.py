from dash.dependencies import Input, Output
from app import app
from computation import compute_survival

@app.callback(Output(component_id = 'disease', component_property = 'options'),
              [Input(component_id = 'tabs', component_property = 'value')])
def render_tab_content(tab):
    if tab == 'CAD':
        return [
                {'label': 'Coronary Artery Disease', 'value': 'CAD'},
                {'label': 'Breast Cancer', 'value': 'BC'},
                {'label': 'Colorectal Cancer', 'value': 'CC'}
                    ]
    elif tab == 'BC':
        return [
                {'label': 'Coronary Artery Disease', 'value': 'CAD'},
                {'label': 'Breast Cancer', 'value': 'BC'},
                {'label': 'Colorectal Cancer', 'value': 'CC'}
                    ]
    elif tab == 'CC':
        return [
                {'label': 'Coronary Artery Disease', 'value': 'CAD'},
                {'label': 'Breast Cancer', 'value': 'BC'},
                {'label': 'Colorectal Cancer', 'value': 'CC'}
                    ]

#breast cancer
@app.callback(Output(component_id = '', component_property = 'options'),
              [Input(component_id = 'tabs', component_property = 'value')])
def update_value(tab):
	return 



#wrap a callback function using decorator. callback is func that gets called once the user input submit some info
@app.callback(
    Output(component_id='survival-plot', component_property='figure'),
    [Input(component_id='tabs', component_property='value')]
    )
def update_graph(tab):
    title = ''
    if tab == 'CAD':
        return {
        'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
            ],
        'layout': {
                'title': 'Survival Probability of ' + title
            }
        }
    elif tab == 'BC':
        return {
        'data': [
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
        'layout': {
                'title': 'Survival Probability of ' + title
            }
        }
    elif tab == 'CC':
        return {
        'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
        'layout': {
                'title': 'Survival Probability of ' + title
            }
        }






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