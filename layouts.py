import dash_core_components as dcc
import dash_html_components as html

layout1 = html.Div(children =[
    html.Label('PRS'),
    dcc.Input(value = '', type = 'text'),

    html.Label('Check if you have'),
    dcc.Checklist(
            options = [
            {'label': 'Severe obsesity', 'value': 'obese'},
            {'label': 'Family history', 'value': 'fam_his'}]),

    html.Label('Variant'),
    dcc.Dropdown(id = 'disease',value=''),
            
    html.P([
        dcc.Graph(
        id='survival-plot',
        config={
                'modeBarButtonsToRemove': ['autoScale2d', 'select2d', 'zoom2d',
                                           'pan2d', 'toggleSpikelines',
                                           'hoverCompareCartesian',
                                           'zoomOut2d', 'zoomIn2d',
                                           'hoverClosestCartesian',
                                           # 'sendDataToCloud',
                                           'resetScale2d']
        })
       ])
    ])


#Breast Cancer
layout2 = html.Div(children =[
    html.Label('Family history'),
    dcc.Input(value = '', type = 'text'),

    html.Label('C1'),
    dcc.Input(value = '', type = 'text'),

    html.Label('C2'),
    dcc.Input(value = '', type = 'text'),

    html.Label('Check if you have'),
    dcc.Checklist(
            options = [
            {'label': 'Severe obsesity', 'value': 'obese'},
            {'label': 'Family history', 'value': 'fam_his'}]),

    html.Label('Variant'),
    dcc.Dropdown(id = 'disease',value=''),
            
    html.P([
        dcc.Graph(
        id='survival-plot',
        config={
                'modeBarButtonsToRemove': ['autoScale2d', 'select2d', 'zoom2d',
                                           'pan2d', 'toggleSpikelines',
                                           'hoverCompareCartesian',
                                           'zoomOut2d', 'zoomIn2d',
                                           'hoverClosestCartesian',
                                           # 'sendDataToCloud',
                                           'resetScale2d']
        })
       ])
    ])



layout3 = html.Div(children =[
    html.Label('TB'),
    dcc.Input(value = '', type = 'text'),

    html.Label('Check if you have'),
    dcc.Checklist(
            options = [
            {'label': 'Severe obsesity', 'value': 'obese'},
            {'label': 'Family history', 'value': 'fam_his'}]),

    html.Label('Variant'),
    dcc.Dropdown(id = 'disease',value=''),
            
    html.P([
        dcc.Graph(
        id='survival-plot',
        config={
                'modeBarButtonsToRemove': ['autoScale2d', 'select2d', 'zoom2d',
                                           'pan2d', 'toggleSpikelines',
                                           'hoverCompareCartesian',
                                           'zoomOut2d', 'zoomIn2d',
                                           'hoverClosestCartesian',
                                           # 'sendDataToCloud',
                                           'resetScale2d']
        })
       ])
    ])
