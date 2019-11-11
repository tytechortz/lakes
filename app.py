import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
import time
from datetime import datetime


today = time.strftime("%Y-%m-%d")

df_powell = pd.read_csv('https://water.usbr.gov/api/web/app.php/api/series?sites=lakepowell&parameters=Day.Inst.ReservoirStorage.af&start=1850-01-01&end='+ today +'&format=csv', skiprows=4)
df_powell['Date'] = pd.to_datetime(df_powell['Date'])
df_powell.set_index(['Date'], inplace=True)
print(df_powell)
df_lp = df_powell.iloc[::-1]
print(df_lp)
# df_lp['Date'] = pd.to_datetime(df_lp['Date'])

# print(df_lp)
levels = df_lp['Value']
# print(levels)
# print(df_lp.iloc[1000,3])
# print(df_lp['Value'])
def get_layout():
    return html.Div(
        [
            html.Div([
                dcc.Graph(
                    id='lake-levels',
                )
            ],
                className='row'
            ),
            html.Div([
                dcc.Dropdown(
                    id='lake',
                    options=[
                        {'label': 'Lake Powell', 'value': 'lp'}
                    ]
                )
            ])
        ]
    )

app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True

@app.callback(
    Output('lake-levels', 'figure'),
    [Input('lake', 'value')])
def lakepowell_graph(lake):
    print(lake)
    traces = []
    if lake == 'lp':
        traces.append(go.Scatter(
            y = df_lp['Value'],
            x = df_lp.index,
        ))
    
    layout = go.Layout(
        height = 500
    )
    return {'data': traces, 'layout': layout}

if __name__ == "__main__":
    app.run_server(port=8020, debug=False)