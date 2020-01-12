import os
import psycopg2
import dash

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets= external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True




    
    
