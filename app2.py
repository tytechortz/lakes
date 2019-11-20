import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
import time
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine
from connect import flaminggorge, powell_latest, powell
# from data_load import ld

capacities = {'LAKE POWELL': 24322000, 'Lake Mead': 26134000, 'FLAMING GORGE RESERVOIR': 3788700, 'NAVAJO RESERVOIR': 1708600, 'BLUE MESA RESERVOIR': 940800 }

def get_layout():
    return html.Div([
        html.Div([
                html.H4('Colorado River Reservoir Levels',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div('Select Reservoir', style={'text-align': 'center'}),
                        dcc.Dropdown(
                        id='lake',
                        options=[
                            {'label': 'Powell', 'value': 'lakepowell'},
                            {'label': 'Mead', 'value': 'hdmlc'},
                            {'label': 'Mead + Powell', 'value': 'combo'},
                            {'label': 'Flaming Gorge', 'value': 'flaminggorge'},
                            {'label': 'Navajo', 'value': 'navajo'},
                            {'label': 'Blue Mesa', 'value': 'bluemesa'},
                        ],
                        value='lakepowell'
                        ),
                    ],
                        className='pretty_container'
                    ),
                ],
                    className='three columns'
                ),
            ],
                className='row'
            ),
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
                        dcc.RadioItems(
                            id='period',
                            options=[
                                {'label':'D', 'value':'1'},
                                {'label':'W', 'value':'7'},
                                {'label':'Y', 'value':'365'},
                            ],
                            value='1',
                            labelStyle={'display': 'inline'},
                            ), 
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
            ],
                className='row'
            ),
            html.Div(id='selected-data', style={'display': 'none'}),
            html.Div(id='current-volume', style={'display': 'none'}),
            html.Div(id='site', style={'display': 'none'}),
            html.Div(id='cvd', style={'display': 'none'}),
    ])


app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True

@app.callback(
    [Output('current-volume', 'children'),
    Output('site', 'children'),
    Output('cvd', 'children')],
    [Input('lake', 'value'),
    Input('selected-data', 'children')])
def get_current_volume(lake, data):
    data = pd.read_json(data)
    print(data.columns)
    data['4'] = pd.to_datetime(data['4'])
    print(data)
    data.set_index(['4'], inplace=True)
    print(data)
    site = data.iloc[0, 1]
    # print(data.iloc[0,3])
    # print(data.iloc[1,3])
    if data.iloc[0,3] == 0:
        current_volume = data.iloc[1,4]
        current_volume_date = data.index[1]
    else:
        current_volume = data.iloc[0,4]
        current_volume_date = data.index[0]
    cvd = str(current_volume_date)
    print(type(cvd))

    return current_volume, site, cvd

@app.callback(
    Output('stats', 'children'),
    [Input('lake', 'value'),
    Input('site', 'children'),
    Input('current-volume', 'children'),
    Input('cvd', 'children')])
def produce_stats(lake, site, data, date ):
    print(data)
    fill_pct = data / capacities[site]
    date = date[0:11]
    # print(date)
    # print(data)
    
    return html.Div([
                html.Div('{} Volume'.format(date), style={'text-align':'center'}),
                html.Div('{:,.0f}'.format(data), style={'text-align':'center'}),
                html.Div('Percent Full', style={'text-align':'center'}),
                html.Div('{0:.0%}'.format(fill_pct), style={'text-align':'center'}),
            ],
                className='round1'
            ),



@app.callback(
    Output('selected-data', 'children'),
    [Input('lake', 'value')])
def clean_data(lake):
    df = pd.DataFrame(powell)

    if lake == 'hdmlc':
        df['1090'] = 10857000
        df['1075'] = 9601000
        df['1050'] = 7683000
        # df['1045'] = 7326000
        # df['1040'] = 6978000
        # df['1035'] = 6638000
        # df['1030'] = 6305000
        df['1025'] = 5981000
    elif lake == 'lakepowell':
        df['power level'] = 6124000

    return df.to_json()

@app.callback(
    Output('lake-levels', 'figure'),
    [Input('lake', 'value'),
    Input('selected-data', 'children')])
def lake_graph(lake, data):
    data = pd.read_json(data)
    data.iloc[:,4] = pd.to_datetime(data.iloc[:,4])
    data.set_index(data.iloc[:,4], inplace=True)
    df = data.sort_index()

    traces = []

    if lake == 'hdmlc':
        for column in data.columns[3:]:
            traces.append(go.Scatter(
                y = df[column],
                x = df.index,
                name = column
            ))
    elif lake == 'lakepowell':
        traces.append(go.Scatter(
            y = df['5'],
            x = df.index,
            name='Water Level'
        )),
        traces.append(go.Scatter(
            y = df['power level'],
            x = df.index,
            name = 'Power level'
        )),
    else:
        traces.append(go.Scatter(
            y = df['Value'],
            x = df.index,
            name='Water Level'
        )),

    layout = go.Layout(
        height =400,
        title = df['1'][0],
        yaxis = {'title':'Volume (AF)'},
    )
    return {'data': traces, 'layout': layout}


if __name__ == "__main__":
    app.run_server(port=8020, debug=False)