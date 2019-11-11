import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
import time
from datetime import datetime


today = time.strftime("%Y-%m-%d")

# levels = df_lp['Value']

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
                html.Div([
                    dcc.Dropdown(
                        id='lake',
                        options=[
                            {'label': 'Lake Powell', 'value': 'lakepowell'},
                            {'label': 'Lake Mead', 'value': 'hdmlc'},
                        ]
                    ),
                ],
                    className='three columns'
                ), 
            ],
                className='row'
            ),
            html.Div(id='selected-data', style={'display': 'none'}),
        ]
    )

app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True

@app.callback(
    Output('selected-data', 'children'),
    [Input('lake', 'value')])
def clean_data(lake):
    df = pd.read_csv('https://water.usbr.gov/api/web/app.php/api/series?sites='+ lake +'&parameters=Day.Inst.ReservoirStorage.af&start=1850-01-01&end='+ today +'&format=csv', skiprows=4)
    if lake == 'hdmlc':
        df['1090'] = 10857000
        df['1075'] = 9601000
        df['1050'] = 7683000
        df['1045'] = 7326000
        df['1040'] = 6978000
        df['1035'] = 6638000
        df['1030'] = 6305000
        df['1025'] = 5981000

    return df.to_json()

@app.callback(
    Output('lake-levels', 'figure'),
    [Input('lake', 'value'),
    Input('selected-data', 'children')])
def lake_graph(lake, data):
    data = pd.read_json(data)
    print(data)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date'], inplace=True)
    print(data)
    traces = []

    if lake == 'hdmlc':
        for column in data.columns[3:]:
            traces.append(go.Scatter(
                y = data[column],
                x = data.index,
                name = column
            ))
    else:
        traces.append(go.Scatter(
            y = data['Value'],
            x = data.index,
            name='Water Level'
        )),
    # traces.append(go.Scatter(
    #     y = data['1090'],
    #     x = data.index,
    # )),
    # traces.append(go.Scatter(
    #     y = data['1075'],
    #     x = data.index,
    # )),
    layout = go.Layout(
        height = 500,
        title = data['Site'][0]
    )
    return {'data': traces, 'layout': layout}

if __name__ == "__main__":
    app.run_server(port=8020, debug=False)