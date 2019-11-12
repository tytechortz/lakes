import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
import time
from datetime import datetime


today = time.strftime("%Y-%m-%d")

capacities = {'LAKE POWELL': 24322000, 'Lake Mead': 26134000, 'FLAMING GORGE RESERVOIR': 3788700, 'NAVAJO RESERVOIR': 1708600, 'BLUE MESA RESERVOIR': 940800 }

# levels = df_lp['Value']

def get_layout():
    return html.Div(
        [
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='lake-levels',
                    ),
                ],
                    className='nine columns'
                ),
                html.Div([
                    html.Div([
                        html.Div(id='stats') 
                    ],
                        className='round1'
                    ),
                    html.Div([
                        html.Div(id='changes') 
                    ],
                        className='round1'
                    ),
                ],
                    className='three columns'
                ),
            #     html.Div([
            #         html.Div([
            #             html.Div(id='changes') 
            #         ],
            #             className='round1'
            #         ),
            #     ],
            #     ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='lake',
                        options=[
                            {'label': 'Powell', 'value': 'lakepowell'},
                            {'label': 'Mead', 'value': 'hdmlc'},
                            {'label': 'Flaming Gorge', 'value': 'flaminggorge'},
                            {'label': 'Navajo', 'value': 'navajo'},
                            {'label': 'Blue Mesa', 'value': 'bluemesa'},
                        ],
                        value='lakepowell'
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
    elif lake == 'lakepowell':
        df['power level'] = 6124000

    return df.to_json()

@app.callback(
    Output('stats', 'children'),
    [Input('lake', 'value'),
    Input('selected-data', 'children')])
def produce_stats(lake, data):
    data = pd.read_json(data)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date'], inplace=True)
    fill_pct = data.iloc[0,3] / capacities[data['Site'][0]]
    print(data)
    print(data.iloc[0,3])
    print(data['Value'][1])
    print(capacities[data['Site'][0]])
    print(fill_pct)
    return html.Div([
                html.Div('Current Volume', style={'text-align':'center'}),
                html.Div('{:,.0f}'.format(data.iloc[0,3]), style={'text-align':'center'}),
                html.Div('Percent Full', style={'text-align':'center'}),
                html.Div('{0:.0%}'.format(fill_pct), style={'text-align':'center'}),
            ],
                className='round1'
            ),

@app.callback(
    Output('lake-levels', 'figure'),
    [Input('lake', 'value'),
    Input('selected-data', 'children')])
def lake_graph(lake, data):
    data = pd.read_json(data)
    # print(data)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date'], inplace=True)
    # print(data)
    traces = []

    if lake == 'hdmlc':
        for column in data.columns[3:]:
            traces.append(go.Scatter(
                y = data[column],
                x = data.index,
                name = column
            ))
    elif lake == 'lakepowell':
        traces.append(go.Scatter(
            y = data['Value'],
            x = data.index,
            name='Water Level'
        )),
        traces.append(go.Scatter(
            y = data['power level'],
            x = data.index,
            name = 'Power level'
        )),
    else:
        traces.append(go.Scatter(
            y = data['Value'],
            x = data.index,
            name='Water Level'
        )),

    layout = go.Layout(
        height = 500,
        title = data['Site'][0]
    )
    return {'data': traces, 'layout': layout}

if __name__ == "__main__":
    app.run_server(port=8020, debug=False)