import dash_core_components as dcc
import dash_html_components as html

#Coronary Artery Disease
# variant sample: 19-11200228-G-C

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

COVARIATES = ['PRS', 'Family History','log Allele Frequency', 'type']
cov_plot_layout = [setup_covariate_plot(cov)
    for cov in COVARIATES]

#Breast Cancer
layout2 = html.Div( children =[
    html.Div(id='test-output'),
    html.Label('Breast Cancer'),

    html.Label('Gene'),
    dcc.Dropdown(id = 'gene', value='BRCA1', 
      options = [
            {'label': 'BRCA 1', 'value': 'BRCA1'},
            {'label': 'BRCA 2', 'value': 'BRCA2'}]),


    html.Label('Nucleotide Position (e.g. 41197701)'),
    dcc.Input(id= 'n_pos', value = 41197701, type = 'number'),

    html.Label('Alteration: Reference -> Mutation (e.g. G-A)'),
    dcc.Input(id= 'alt', value = 'G-A' , type = 'text'),

    html.Label('Basic Health Info: Check if you have'),
    html.Div(
      #style={'width':'10%', 'height':'100%','float':'left'},
      children = [
          dcc.Checklist(
            id= 'obese-hist',
            options = [
            {'label': 'Severe obsesity', 'value': 'obese'},
            {'label': 'Family history', 'value': 'fam_his'}],
            value = ['default'],
            labelStyle = {'display': 'block'}),
      ]),
    html.Div(id='prs'),
    dcc.Slider(
      id = 'prs-slider',
      min=-5,
      max=5,
      step = 0.1,
      #marks={i: str(i) for i in range(-5,6)},
      marks={i/2: str(i/2) for i in range(-10,12)},
      value=0,
    ),

            
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
        }),
        
    html.Div(
        cov_plot_layout,

       ),  
    ])

#Colerect Cancer
# variant sample : 2-47630331-A-C
layout3 = html.Div(children =[
    html.Div(id='test-output'),
    html.Label('Colorectal Cancer'),

    html.Label('Gene'),
    dcc.Dropdown(id = 'gene',value='MSH2', 
      options = [
            #msh2, msh6, pms2, mlh1
            {'label': 'MSH 2', 'value': 'MSH2'},
            {'label': 'MSH 6', 'value': 'MSH6'},
            {'label': 'PMS 2', 'value': 'PMS2'},
            {'label': 'MLH 1', 'value': 'MLH1'}]),

    html.Label('Nucleotide Position (e.g. 47630331)'),
    dcc.Input(id= 'n_pos', value = 47630331, type = 'number'),

    html.Label('Alteration: Reference -> Mutation (e.g. A-C)'),
    dcc.Input(id= 'alt', value = 'A-C' , type = 'text'),

    html.Label('Basic Health Info: Check if you have'),
    html.Div(
      #style={'width':'10%', 'height':'100%','float':'left'},
      children = [
          dcc.Checklist(
            id= 'obese-hist',
            options = [
            {'label': 'Severe obsesity', 'value': 'obese'},
            {'label': 'Family history', 'value': 'fam_his'}],
            value = ['default'],
            labelStyle = {'display': 'block'}),
      ]),
    html.Div(id='prs'),
    dcc.Slider(
      id = 'prs-slider',
      min=-5,
      max=5,
      step = 0.1,
      marks={i/2: str(i/2) for i in range(-10,12)},
      #marks={i: 'Label {}'.format(i) for i in range(-50,60)},
      value=0,
    ),
    
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
        }),

    
    html.P([
        dcc.Graph(
        id='covariate-plot1',
        config={
                'modeBarButtonsToRemove': ['autoScale2d', 'select2d', 'zoom2d',
                                           'pan2d', 'toggleSpikelines',
                                           'hoverCompareCartesian',
                                           'zoomOut2d', 'zoomIn2d',
                                           'hoverClosestCartesian',
                                           # 'sendDataToCloud',
                                           'resetScale2d']
        }),
        dcc.Graph(
        id='covariate-plot',
        config={
                'modeBarButtonsToRemove': ['autoScale2d', 'select2d', 'zoom2d',
                                           'pan2d', 'toggleSpikelines',
                                           'hoverCompareCartesian',
                                           'zoomOut2d', 'zoomIn2d',
                                           'hoverClosestCartesian',
                                           # 'sendDataToCloud',
                                           'resetScale2d']
        })
       ],  style = {'width': 1000 })
    
    
    
    
    ])

    
layout1 = html.Div(children =[
    html.Div(id='test-output'),
    html.Label('Coronary Artery Disease'),

    html.Label('Gene'),
    dcc.Dropdown(id = 'gene',value='LDLR', 
      options = [
            # LDLR, APOB, pcsk9
            {'label': 'LDLR', 'value': 'LDLR'},
            {'label': 'APOB', 'value': 'APOB'},
            {'label': 'PCSK 9', 'value': 'PCSK9'}]),

    html.Label('Nucleotide Position (e.g. 11200228)'),
    dcc.Input(id= 'n_pos', value =11200228, type = 'number', placeholder = 11200228),

    html.Label('Alteration: Reference -> Mutation (e.g. G-C)'),
    dcc.Input(id= 'alt', value = 'G-C' , type = 'text', placeholder = 'G-C'),

    html.Label('Basic Health Info: Check if you have'),
    html.Div(
      #style={'width':'10%', 'height':'100%','float':'left'},
      children = [
          dcc.Checklist(
            id= 'obese-hist',
            options = [
            {'label': 'Severe obsesity', 'value': 'obese'},
            {'label': 'Family history', 'value': 'fam_his'}],
            value = ['default'],
            labelStyle = {'display': 'block'}),
      ]),
    html.Div(id='prs'),
    dcc.Slider(
      id = 'prs-slider',
      min=-5,
      max=5,
      step = 0.1,
      marks={i/2: str(i/2) for i in range(-10,12)},

      #marks={i/10: 'Label {}'.format(i/10) for i in range(0,50)},
      value=0,
    ),
    
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
        }),

            
    html.P(

        dcc.Graph(
        id='covariate-plot',
        config={
                'modeBarButtonsToRemove': ['autoScale2d', 'select2d', 'zoom2d',
                                           'pan2d', 'toggleSpikelines',
                                           'hoverCompareCartesian',
                                           'zoomOut2d', 'zoomIn2d',
                                           'hoverClosestCartesian',
                                           # 'sendDataToCloud',
                                           'resetScale2d']
        },
        style = {'width': 1000 })
       )
    ])