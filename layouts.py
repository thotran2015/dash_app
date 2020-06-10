import dash_core_components as dcc
import dash_html_components as html
from layout_util import setup_default_menu, setup_covariate_plot, setup_survival_plot, setup_ph_plot

#Coronary Artery Disease
# variant sample: 19-11200228-G-C


COVARIATES = ['PRS', 'Family History','log Allele Frequency', 'type']
cov_plot_layout = [setup_covariate_plot(cov) for cov in COVARIATES]
bgColor = 'lightgrey'
boxSha =  '5px 5px grey'

COV_DISEASE = {'breast cancer': [['Family History', 'log Allele Frequency'], ['Mutations', 'Regions']],
               'colorectal cancer':  [['Family History', 'log Allele Frequency'], ['Mutations', 'Regions']],
               'coronary artery disease' : [['Family History', 'log Allele Frequency'], ['Mutations', 'Regions']]}

def get_hazard_plots_layout(row, col):
    return [html.Div([
        html.Div(
            setup_ph_plot(str(r*row + c)),
            id = 'hazard-ratio-wrapper-'+str(r*row + c), className = 'six columns', style = dict(boxShadow = boxSha))
            for c in range(col)],
        id = 'hazard-ratio-plot-'+str(r), className = 'row', style = dict(backgroundColor = bgColor, padding = '2%', display = 'flex')) for r in range(row)]


    


def get_cov_grp_plots_layout(disease):
    return  [html.Div(
        [html.Div(setup_covariate_plot(str(r*len(row) + i)),
            id = 'cov-group-plot-wrapper-'+str(r*len(row) + i), className = 'six columns',  style = dict(boxShadow = boxSha))
         for i, cov in enumerate(row)],
        id = 'cov-group-plot-'+str(r), className = 'row', style = dict(backgroundColor = bgColor, padding = '2%',  display = 'flex')
       ) for r, row in enumerate(COV_DISEASE[disease])]


def get_template_layout(disease): 
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
    
        ] +get_cov_grp_plots_layout(disease) + get_hazard_plots_layout(2,2)

#Breast Cancer
layout2 = get_template_layout('breast cancer')

#Colerect Cancer
# variant sample : 2-47630331-A-C
layout3 = get_template_layout('colorectal cancer')

    
layout1 = get_template_layout('coronary artery disease')

 # html.Div([
 #        html.Div(
 #            setup_ph_plot('1'),
 #            id = 'hazard-ratio-1-wrapper', className = 'six columns', style = dict(boxShadow = boxSha)),
 #        html.Div(
 #            setup_ph_plot('2'),
 #            id = 'hazard-ratio-2-wrapper', className = 'six columns', style = dict(boxShadow = boxSha)),
 #            ],
 #        id = 'hazard-ratio-plot-1-2', className = 'row', style = dict(backgroundColor = bgColor, padding = '2%', display = 'flex')),

 #    html.Div([
 #        html.Div(
 #            setup_ph_plot('3'),
 #            id = 'hazard-ratio-3-wrapper', className = 'six columns',  style = dict(boxShadow = boxSha)),
 #        html.Div(
 #            setup_ph_plot('4'),
 #            id = 'hazard-ratio-4-wrapper', className = 'six columns',  style = dict(boxShadow = boxSha)),
 #            ],
 #        id = 'hazard-ratio-plot-3-4', className = 'row', style = dict(backgroundColor = bgColor, padding = '2%',  display = 'flex')),
    # html.Div(
    #     [html.Div(setup_covariate_plot(str(i)),
    #         id = 'cov-group-plot-1-wrapper', className = 'six columns',  style = dict(boxShadow = boxSha))
    #      for i, cov in enumerate(covariate_groups[0])],
    #     id = 'cov-group-plot-1-2', className = 'row', style = dict(backgroundColor = bgColor, padding = '2%',  display = 'flex')
    #    ),
    # html.Div(
    #     [html.Div(setup_covariate_plot(str(2+i)),
    #         id = 'cov-group-plot-2-wrapper', className = 'six columns',  style = dict(boxShadow = boxSha))
    #      for i, cov in  enumerate(covariate_groups[1])],
    #     id = 'cov-group-plot-3-4', className = 'row', style = dict(backgroundColor = bgColor, padding = '2%',  display = 'flex')
    #    )