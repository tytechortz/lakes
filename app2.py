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
    ])


app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True


@app.callback(
    Output('selected-data', 'children'),
    [Input('lake', 'value')])
def clean_data(lake):
    df = pd.DataFrame(powell)
    print(df)
    # powell_data[4] = pd.to_datetime(powell_data[4])
    # powell_data = powell_data.set_index([4])
    # dfp = powell_data.sort_index()
    # print(dfp)
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
    # chopped_df = dfp[dfp.Value != 0]
    # print(chopped_df)
    print(df)

    return df.to_json()

@app.callback(
    Output('lake-levels', 'figure'),
    [Input('lake', 'value'),
    Input('selected-data', 'children')])
def lake_graph(lake, data):
    data = pd.read_json(data)
    print(data)
    data.iloc[:,4] = pd.to_datetime(data.iloc[:,4])
    data.set_index(data.iloc[:,4], inplace=True)
    print(data)
  
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
            y = data['5'],
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
        height =400,
        title = data['1'][0],
        yaxis = {'title':'Volume (AF)'},
    )
    return {'data': traces, 'layout': layout}


if __name__ == "__main__":
    app.run_server(port=8020, debug=False)