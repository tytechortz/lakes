import psycopg2
from psycopg2 import pool

try:

    postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20,user = "postgres",
                                                password = "1234",
                                                host = "localhost",
                                                database = "lakes")

    if(postgreSQL_pool):
            print("Connection pool created successfully")

# Use getconn() to Get Connection from connection pool
    powell_connection  = postgreSQL_pool.getconn()
    powell_latest_connection = postgreSQL_pool.getconn()
    mead_connection = postgreSQL_pool.getconn()
    flaminggorge_connection = postgreSQL_pool.getconn()


    if(powell_connection):
        print("successfully recived connection from connection pool ")
        powell_cursor = powell_connection.cursor()
        powell_cursor.execute("SELECT * FROM lake_powell")
        powell = powell_cursor.fetchall()
        powell_cursor.close()

        powell_latest_cursor = powell_latest_connection.cursor()
        powell_latest_cursor.execute("SELECT * FROM lake_powell")
        powell_latest = powell_latest_cursor.fetchone()
        powell_latest_cursor.close()

        flaminggorge_cursor = flaminggorge_connection.cursor()
        flaminggorge_cursor.execute("SELECT * FROM flaming_gorge")
        flaminggorge = flaminggorge_cursor.fetchall()
        flaminggorge_cursor.close()

        print("Put away a PostgreQL connection")
        postgreSQL_pool.putconn(powell_connection)
        postgreSQL_pool.putconn(flaminggorge_connection)

except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connnecting to PostgreSQL", error)

finally:
    if (postgreSQL_pool):
        postgreSQL_pool.closeall
    print("PostgreSQL connection pool is closed")

