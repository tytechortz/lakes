import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import time


today = time.strftime("%Y-%m-%d")

app = dash.Dash(__name__)

df_lp = pd.read_csv('https://water.usbr.gov/api/web/app.php/api/series?sites=lakepowell&parameters=Day.Inst.ReservoirStorage.af&start=1850-01-01&end='+ today +'&format=csv', skiprows=4)

print(df_lp)