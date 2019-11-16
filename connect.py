import psycopg2
from psycopg2 import pool

try:

    postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20,user = "postgres",
                                                password = "1234",
                                                host = "localhost",
                                                database = "denver_temps")

    if(postgreSQL_pool):
            print("Connection pool created successfully")

# Use getconn() to Get Connection from connection pool
    powell_connection  = postgreSQL_pool.getconn()
    mead_connection = postgreSQL_pool.getconn()

    if(powell_connection):
        print("successfully recived connection from connection pool ")
        powell_cursor = powell_connection.cursor()
        powell_cursor.execute("select")