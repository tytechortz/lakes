import psycopg2
import pandas as pd
import sqlalchemy
import time

# today = time.strftime("%Y-%m-%d")

# df = pd.read_csv('https://water.usbr.gov/api/web/app.php/api/series?sites=lakepowell&parameters=Day.Inst.ReservoirStorage.af&start=1850-01-01&end=2019-11-1&format=csv', skiprows=4)
# print(df)
# engine = sqlalchemy.create_engine("postgresql://postgres:1234@localhost/lakes")
# con = engine.connect()

# table_name = 'flaming_gorge'
# df.to_sql(table_name, con)
# print(engine.table_names())

# con.close()

# engine = sqlalchemy.create_engine("postgresql://postgres:1234@localhost/lakes")
# con = engine.connect()

# print(engine.table_names())

# table_name = 'lake_powell'
# df.to_sql(table_name, con)
# print(engine.table_names())

# con.close()