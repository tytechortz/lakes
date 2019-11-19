import pandas as pd
import psycopg2
from connect import powell_latest
import time
from sqlalchemy import create_engine

today = time.strftime("%Y-%m-%d")

last_day = powell_latest[4][:11]

def update_data():
    data = pd.read_csv('https://water.usbr.gov/api/web/app.php/api/series?sites=lakepowell&parameters=Day.Inst.ReservoirStorage.af&start=1850-01-01&end=2019-11-15&format=csv', skiprows=4)
    # print(data)
    
    engine = create_engine('postgresql://postgres:1234@localhost:5432/lakes')
    data.to_sql('lake_powell', engine, if_exists='append')


    return data    

update_data()

powell_data = update_data()


