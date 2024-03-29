import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
import time
from datetime import datetime
from sqlalchemy import create_engine
from connect import powell, flaminggorge


today = time.strftime("%Y-%m-%d")

capacities = {'LAKE POWELL': 24322000, 'Lake Mead': 26134000, 'FLAMING GORGE RESERVOIR': 3788700, 'NAVAJO RESERVOIR': 1708600, 'BLUE MESA RESERVOIR': 940800 }

def get_layout():
    return html.Div(
        [
            html.Div([
                html.H4('Colorado River Reservoir Levels',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
                html.Button('Update Data', id='data-button'),
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
            
            html.Div([
                html.P(
                    '',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='annual-bars',
                    ),
                ],
                    className='nine columns'
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
            html.Div(id='cvd', style={'display': 'none'}),
            html.Div(id='sorted-year-end', style={'display': 'none'}),
            html.Div(id='annual-max', style={'display': 'none'}),
            html.Div(id='annual-min', style={'display': 'none'}),
            html.Div(id='output-data-button', style={'display': 'none'}),
        ]
    )

app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True

@app.callback(Output('output-data-button', 'children'),
             [Input('data-button', 'n_clicks')])
def update_data(n_clicks):
    print(n_clicks)
    data = pd.read_csv('https://water.usbr.gov/api/web/app.php/api/series?sites=flaminggorge&parameters=Day.Inst.ReservoirStorage.af&start=1850-01-01&end=2019-11-02&format=csv', skiprows=4)

    print(data)

    # most_recent_data_date = last_day - timedelta(days=1)
    # mrd = most_recent_data_date.strftime("%Y-%m-%d")


    # print(most_recent_data_date)
    engine = create_engine('postgresql://postgres:1234@localhost:5432/lakes')
    data.to_sql('flaming_gorge', engine, if_exists='append')

    return "Data Updated"

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
    # print(chopped_df)
    print(chopped_df)

    return chopped_df.to_json()


@app.callback(
    Output('annual-max-table', 'children'),
    [Input('annual-max', 'children')])
def record_water_table(data):
    data = pd.read_json(data)
    sorted_annual_max_all = data.sort_values(by='Value', axis=0, ascending=True)
   
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
    [Input('annual-min', 'children')])
def record_water_table(data):
    data = pd.read_json(data)
    # print(data)
    sorted_annual_min_all = data.sort_values(by='Value', axis=0, ascending=True)
   
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
    [Output('sorted-year-end', 'children'),
    Output('annual-max', 'children'),
    Output('annual-min', 'children')],
    [Input('selected-data', 'children')])
def data_factory(data):
    data = pd.read_json(data)
    # print(data)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date'], inplace=True)
    data_twok = data[(data.index.year > 1999)]
    # print(data_twok)
    year_end = data_twok[(data_twok.index.month == 12) & (data_twok.index.day == 31)]
    # sorted_year_end = year_end.sort_values(by='Value', axis=0, ascending=False)

    annual_max_all = data.resample('Y').max()
    annual_max_twok = annual_max_all[(annual_max_all.index.year > 1999)]
    # sorted_annual_max = annual_max_twok.sort_values(by='Value', axis=0, ascending=True)

    annual_min_all = data.resample('Y').min()
    annual_min_twok = annual_min_all[(annual_min_all.index.year > 1999)]
    # sorted_annual_min = annual_min_twok.sort_values(by='Value', axis=0, ascending=True)

    return year_end.to_json(), annual_max_twok.to_json(), annual_min_twok.to_json()

@app.callback(
    Output('year-end-table', 'children'),
    [Input('sorted-year-end', 'children')])
def year_end_table(data):
    data = pd.read_json(data)
    # print(data)
    # print(data.index[0].year)
    sorted_year_end = data.sort_values(by='Value', axis=0, ascending=True)
   
    return html.Div([
                html.Div('Year End', style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div('{}'.format(sorted_year_end.index[y].year), style={'text-align': 'center'}) for y in range(len(sorted_year_end))
                        ],
                            className='four columns'
                        ),
                        html.Div([
                            html.Div('{:,.0f}'.format(sorted_year_end.iloc[y,3]), style={'text-align': 'center'}) for y in range(len(sorted_year_end))
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
                html.Div([
                    html.Div(id='year-end-table')
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
    change = current_data - past_data
    annual_min = data.resample('Y').min()
    annual_min_twok = annual_min[(annual_min.index.year > 1999)]
    rec_low = annual_min_twok['Value'].min()
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
    Output('site', 'children'),
    Output('cvd', 'children')],
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
        current_volume_date = data.index[1]
    else:
        current_volume = data.iloc[0,3]
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
        height =400,
        title = data['Site'][0],
        yaxis = {'title':'Volume (AF)'},
    )
    return {'data': traces, 'layout': layout}

@app.callback(
    Output('annual-bars', 'figure'),
    [Input('sorted-year-end', 'children'),
    Input('annual-max', 'children'),
    Input('annual-min', 'children')])
def lake_graph(ye_data, max_data, min_data):
    year_end = pd.read_json(ye_data)
    max_data = pd.read_json(max_data)
    min_data = pd.read_json(min_data)

    traces = []

    trace_data = [max_data, min_data, year_end]
    titles = ['Max', 'Min', 'Year End']

    x = 0
    for i in trace_data:
        traces.append(
            go.Bar(
                x=i.index,
                y=i['Value'],
                name=titles[x]
            )
        )
        x += 1
        
    layout = go.Layout(
        height = 400,
        title = '{}, 2000-Present'.format(year_end.iloc[0,0]),
        yaxis = {'title':'Volume (AF)'},
    )
    return {'data': traces, 'layout': layout}

if __name__ == "__main__":
    app.run_server(port=8020, debug=False)