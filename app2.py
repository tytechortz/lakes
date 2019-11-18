import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
import time
from datetime import datetime
from sqlalchemy import create_engine
from connect import flaminggorge, powell_latest, powell


# powell_data = pd.DataFrame(powell)
# print(powell_data)
print(powell_latest)
print(powell_latest[4][:11])


def get_layout():
    return html.Div([
        html.Div([
                html.H4('Colorado River Reservoir Levels',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
                html.Button('Update Data', id='data-button'),
            ],
                className='row'
            ),
    ])


app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True


if __name__ == "__main__":
    app.run_server(port=8020, debug=False)