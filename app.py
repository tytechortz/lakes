import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import time


today = time.strftime("%Y-%m-%d")

df_lp = pd.read_csv('https://water.usbr.gov/api/web/app.php/api/series?sites=lakepowell&parameters=Day.Inst.ReservoirStorage.af&start=1850-01-01&end='+ today +'&format=csv', skiprows=4)

print(df_lp)

def get_layout():
    return html.Div(
        [
            dcc.Graph(
                data = go.Scatter(
                y = df_lp['Value'],
                x = df_lp['Date'],
                ),
                layout = go.Layout(
                height = 500
                )
            )
        ]
    )

app = dash.Dash(__name__)
app.layout = get_layout
app.config['suppress_callback_exceptions']=True

# @app.callback(
#     Output('graph', 'figure'),
#     [Input('')
# )
# def lakepowell_graph():
#     data = go.Scatter(
#         y = df_lp['Value'],
#         x = df_lp['Date'],
#     )
#     layout = go.Layout(
#         height = 500
#     )
#     return {'data': data, 'layout': layout}

if __name__ == "__main__":
    app.run_server(port=8020, debug=False)