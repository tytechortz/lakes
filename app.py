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
            html.Div([
                html.Div([
                    html.Div(
                        id='rankings'
                    ), 
                ],
                    className='twelve columns'
                ),
            ],
                className='row'
            ),
            html.Div(id='selected-data', style={'display': 'none'}),
            html.Div(id='current-volume', style={'display': 'none'}),
            html.Div(id='site', style={'display': 'none'}),
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
        # df['1045'] = 7326000
        # df['1040'] = 6978000
        # df['1035'] = 6638000
        # df['1030'] = 6305000
        df['1025'] = 5981000
    elif lake == 'lakepowell':
        df['power level'] = 6124000
    chopped_df = df[df.Value != 0]
    print(chopped_df)

    return chopped_df.to_json()


@app.callback(
    Output('annual-max-table', 'children'),
    [Input('selected-data', 'children')])
def record_water_table(data):
    data = pd.read_json(data)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date'], inplace=True)

    annual_max_all = data.resample('Y').max()
    annual_max_twok = annual_max_all[(annual_max_all.index.year > 1999)]
    sorted_annual_max_all = annual_max_twok.sort_values(by='Value', axis=0, ascending=True)
   
    return html.Div([
                html.Div('Annual Max', style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div('{}'.format(sorted_annual_max_all.index[y].year), style={'text-align': 'center'}) for y in range(len(sorted_annual_max_all))
                        ],
                            className='four columns'
                        ),
                        html.Div([
                            html.Div('{:,.0f}'.format(sorted_annual_max_all.iloc[y,3]), style={'text-align': 'center'}) for y in range(len(sorted_annual_max_all))
                        ],
                            className='eight columns'
                        ),  
                    ],
                        className='row'
                    ),
                ],
                    className='round1'
                ),      
            ],
                className='round1'
            )

@app.callback(
    Output('annual-min-table', 'children'),
    [Input('selected-data', 'children')])
def record_water_table(data):
    data = pd.read_json(data)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date'], inplace=True)

    annual_min_all = data.resample('Y').min()
    annual_min_twok = annual_min_all[(annual_min_all.index.year > 1999)]
    sorted_annual_min_all = annual_min_twok.sort_values(by='Value', axis=0, ascending=True)
   
    return html.Div([
                html.Div('Annual Min', style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div('{}'.format(sorted_annual_min_all.index[y].year), style={'text-align': 'center'}) for y in range(len(sorted_annual_min_all))
                        ],
                            className='four columns'
                        ),
                        html.Div([
                            html.Div('{:,.0f}'.format(sorted_annual_min_all.iloc[y,3]), style={'text-align': 'center'}) for y in range(len(sorted_annual_min_all))
                        ],
                            className='eight columns'
                        ),  
                    ],
                        className='row'
                    ),
                ],
                    className='round1'
                ),      
            ],
                className='round1'
            )

@app.callback(
    Output('rankings', 'children'),
    [Input('selected-data', 'children')])
def display_stats(value):
    # print(value)
    return html.Div([
            html.Div([
                html.Div([
                    html.Div(id='annual-max-table')
                ],
                    className='two columns'
                ),
                html.Div([
                    html.Div(id='annual-min-table')
                ],
                    className='two columns'
                ),
            ])
    ],
        className='twelve columns'
    ),

@app.callback(
    Output('changes', 'children'),
    [Input('lake', 'value'),
    Input('period', 'value'),
    Input('selected-data', 'children')])
def produce_changes(lake, period, data):
    data = pd.read_json(data)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date'], inplace=True)
    current_data = data.iloc[0,3]
    past_data = data.iloc[int(period),3]
    # if data.iloc[0,3] == 0:
    #     current_data = data.iloc[1,3]
    #     past_data = data.iloc[int(period)+1,3]
    # else:
    #     current_data == data.iloc[0,3]
    #     past_data = data.iloc[int(period),3]
    # print(current_data)
    # print(past_data)
    change = current_data - past_data
    annual_min = data.resample('Y').min()
    annual_min_twok = annual_min[(annual_min.index.year > 1999)]
    rec_low = annual_min_twok['Value'].min()
    # print(rec_low)
    dif_rl = data.iloc[0,3] - rec_low
 

    return html.Div([
                html.Div('Change', style={'text-align':'center'}),
                html.Div('{:,.0f}'.format(change), style={'text-align':'center'}),
                html.Div('Record Low', style={'text-align':'center'}),
                html.Div('{:,.0f}'.format(rec_low), style={'text-align':'center'}),
                html.Div('Difference', style={'text-align':'center'}),
                html.Div('{:,.0f}'.format(dif_rl), style={'text-align':'center'}),
            ],
                className='round1'
            ),

@app.callback(
    [Output('current-volume', 'children'),
    Output('site', 'children')],
    [Input('lake', 'value'),
    Input('selected-data', 'children')])
def get_current_volume(lake, data):
    data = pd.read_json(data)
    # print(data)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date'], inplace=True)
    site = data.iloc[0, 0]
    # print(data.iloc[0,3])
    # print(data.iloc[1,3])
    if data.iloc[0,3] == 0:
        current_volume = data.iloc[1,3]
    else:
        current_volume = data.iloc[0,3]
    # print(current_volume)

    return current_volume, site

@app.callback(
    Output('stats', 'children'),
    [Input('lake', 'value'),
    Input('site', 'children'),
    Input('current-volume', 'children')])
def produce_stats(lake, site, data):
    # print(data)
    # print(site)
    # data['Date'] = pd.to_datetime(data['Date'])
    # data.set_index(['Date'], inplace=True)

    # if data.iloc[0,3] == 0:
    #     current_volume = data.iloc[1,3]
    # else:
    #     current_volume = data.iloc[0,3]
    fill_pct = data / capacities[site]
    
    # print(data)
    # print(data.iloc[0,3])
    # print(data.iloc[1,3])
    # print(capacities[data['Site'][0]])
    # print(fill_pct)
    return html.Div([
                html.Div('Current Volume', style={'text-align':'center'}),
                html.Div('{:,.0f}'.format(data), style={'text-align':'center'}),
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
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date'], inplace=True)
  
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