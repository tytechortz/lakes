import pandas as pd
import psycopg2
from connect import powell_latest
import time
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine

today = time.strftime("%Y-%m-%d")

last_day = powell_latest[4][:11] 
# ld = last_day.strftime("%Y-%m-%d")
print(last_day)
print(len(last_day))
print(last_day[:10])
ld = last_day[:10]
print(ld)

def update_data():
    data = pd.read_csv('https://water.usbr.gov/api/web/app.php/api/series?sites=lakepowell&parameters=Day.Inst.ReservoirStorage.af&start=' + ld + '&end=2019-11-16&format=csv', skiprows=4)
    print(data)
    
    engine = create_engine('postgresql://postgres:1234@localhost:5432/lakes')
    data.to_sql('lake_powell', engine, if_exists='append')


    return None   

update_data()

# powell_data = update_data()


