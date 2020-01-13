import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from layouts import layout1, layout2, layout3
import callbacks

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

cursor = conn.cursor()

# Print PostgreSQL Connection properties
print ( connection.get_dsn_parameters(),"\n")

# Print PostgreSQL version
cursor.execute("SELECT version();")

app.layout = html.Div(children =[
    html.H1(children = 'Calculate your risk for coronary artery disease, breast cancer, or colorectal cancer',
             style = {'text-align': 'center'}),
    dcc.Tabs(id="tabs", value='BC', children=[
        dcc.Tab(label='Coronary Artery Disease', value='CAD'),
        dcc.Tab(label='Breast Cancer', value='BC'),
        dcc.Tab(label='Colorectal Cancer', value= 'CC')
    ]), 
    html.Div(id='page-content')
    ])

@app.callback(Output(component_id = 'page-content', component_property = 'children'), 
                [Input(component_id = 'tabs', component_property = 'value')])
def render_tab_title(tab):
    if tab =='CAD':
        return layout1
    elif tab == 'BC':
        return layout2
    elif tab == 'CC':
        return layout3

if __name__ == '__main__':
    app.run_server(debug = True)
