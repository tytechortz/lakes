# import pandas as pd
# import psycopg2
# import time
# from datetime import datetime, date, timedelta
# from sqlalchemy import create_engine
# from connect import powell

# today = time.strftime("%Y-%m-%d")

# # df_powell = pd.DataFrame(powell)
# # # print(df_powell)
# # df_powell[4] = pd.to_datetime(df_powell[4])
# # # print(df_powell)
# # dfp = df_powell.set_index([4])
# # sorted_powell = dfp.sort_index()
# # print(sorted_powell)

# # # print(dfp)
# # last_day = sorted_powell.index[-1] + timedelta(days=1)
# # ld = last_day.strftime("%Y-%m-%d")
# # # print(dfp)
# # print(ld)

# def update_data():
#     data = pd.read_csv('https://water.usbr.gov/api/web/app.php/api/series?sites=lakepowell&parameters=Day.Inst.ReservoirStorage.af&start=1850-01-01&end=' + today + '&format=csv', skiprows=4)
#     print(data)
    
#     engine = create_engine('postgresql://postgres:1234@localhost:5432/lakes')
#     con = engine.connect()

#     data.to_sql('lake_powell', engine, if_exists='append')

#     con.close()

#     return None   

# update_data()

# print(sorted_powell)

# powell_data = update_data()


