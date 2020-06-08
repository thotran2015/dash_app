import dash_core_components as dcc
import dash_html_components as html
from layout_util import setup_default_menu, setup_covariate_plot, setup_survival_plot, setup_ph_plot

#Coronary Artery Disease
# variant sample: 19-11200228-G-C


COVARIATES = ['PRS', 'Family History','log Allele Frequency', 'type']
cov_plot_layout = [setup_covariate_plot(cov) for cov in COVARIATES]
bgColor = 'lightgrey'
boxSha =  '5px 5px grey'

COV_DISEASE = {'breast cancer': [['Family History', 'log Allele Frequency'], ['Mutations', 'PRS']],
               'colorectal cancer':  [['Family History', 'log Allele Frequency'], ['Mutations', 'sex']],
               'coronary artery disease' : [['Family History', 'log Allele Frequency'], ['Mutations', 'PRS']]}

def get_template_layout(disease): 
    covariate_groups = COV_DISEASE[disease]
    return [
    html.Div([
        html.Div(
                 setup_default_menu(disease),
                 id = 'menu-wrapper', className = 'six columns', style = dict(backgroundColor = 'white', boxShadow = boxSha)),
            
            html.Div(setup_survival_plot(), id = 'survival-plot-wrapper', className = 'six columns',
                     style = dict(backgroundColor = 'white', boxShadow = boxSha)
                     )
            ],
           id = 'menu-survival-curve', className = 'row', style = dict(backgroundColor = bgColor, padding = '2%', display ='flex')
            ),
    html.Div([
        html.Div(
            setup_ph_plot('1'),
            id = 'hazard-ratio-1-wrapper', className = 'six columns', style = dict(boxShadow = boxSha)),
        html.Div(
            setup_ph_plot('2'),
            id = 'hazard-ratio-2-wrapper', className = 'six columns', style = dict(boxShadow = boxSha)),
            ],
        id = 'hazard-ratio-plot-1-2', className = 'row', style = dict(backgroundColor = bgColor, padding = '2%', display = 'flex')),

    html.Div([
        html.Div(
            setup_ph_plot('3'),
            id = 'hazard-ratio-3-wrapper', className = 'six columns',  style = dict(boxShadow = boxSha)),
        html.Div(
            setup_ph_plot('4'),
            id = 'hazard-ratio-4-wrapper', className = 'six columns',  style = dict(boxShadow = boxSha)),
            ],
        id = 'hazard-ratio-plot-3-4', className = 'row', style = dict(backgroundColor = bgColor, padding = '2%',  display = 'flex')),
        
    html.Div(
        [html.Div(setup_covariate_plot(str(i)),
            id = 'cov-group-plot-1-wrapper', className = 'six columns',  style = dict(boxShadow = boxSha))
         for i, cov in enumerate(covariate_groups[0])],
        id = 'cov-group-plot-1-2', className = 'row', style = dict(backgroundColor = bgColor, padding = '2%',  display = 'flex')
       ),
    html.Div(
        [html.Div(setup_covariate_plot(str(2+i)),
            id = 'cov-group-plot-2-wrapper', className = 'six columns',  style = dict(boxShadow = boxSha))
         for i, cov in  enumerate(covariate_groups[1])],
        id = 'cov-group-plot-3-4', className = 'row', style = dict(backgroundColor = bgColor, padding = '2%',  display = 'flex')
       )
    ]

#Breast Cancer
layout2 = get_template_layout('breast cancer')

#Colerect Cancer
# variant sample : 2-47630331-A-C
layout3 = get_template_layout('colorectal cancer')


    
layout1 = get_template_layout('coronary artery disease')

 # html.Div(id='test-output'),
    # html.Label('Breast Cancer'),
    # html.Label('Gene'),
    # dcc.Dropdown(id = 'gene', value='BRCA1', 
    #   options = [
    #         {'label': 'BRCA 1', 'value': 'BRCA1'},
    #         {'label': 'BRCA 2', 'value': 'BRCA2'}],
    #   style= dict(
    #       width='30%',
    #       verticalAlign="left"
    #             )),


    # html.Label('Nucleotide Position (e.g. 41197701)'),
    # dcc.Input(id= 'n_pos', value = 41197701, type = 'number',    
    #           style= dict(
    #       width='30%',
    #       verticalAlign="left"
    #             )),

    # html.Label('Alteration: Reference -> Mutation (e.g. G>A)'),
    # dcc.Input(id= 'alt', value = 'G>A' , type = 'text', 
    #           style= dict(
    #       width='30%',
    #       verticalAlign="left"
   #             )),
    #html.Label('Basic Health Info: Check if you have'),