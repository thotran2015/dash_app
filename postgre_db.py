import os
from psycopg2 import connect

database_url = os.getenv("DATABASE_URL")
if database_url is not None:
    con = connect(database_url)
else:
    import configparser
    CONFIG = configparser.ConfigParser()
    CONFIG.read('../db.cfg')
    dbset = CONFIG['DBSETTINGS']

    con = connect(**dbset)

HOST = 'ec2-54-235-89-123.compute-1.amazonaws.com'
DB = 'da1e3uq86ab5tu'
USER = 'duozofkhzsfjvy'
POST = 5432
PASSWORD = '46ef1e44c2b9751801126174b41e124a7f1c847b9e0cf2f27af49a0a3278d5db'
URI = 'postgres://duozofkhzsfjvy:46ef1e44c2b9751801126174b41e124a7f1c847b9e0cf2f27af49a0a3278d5db@ec2-54-235-89-123.compute-1.amazonaws.com:5432/da1e3uq86ab5tu'
try:
  connection = psycopg2.connect(host=HOST,dbname=DB, user=USER, password=PASSWORD, sslmode='require')
  #connection = psycopg2.connect(DATABASE_URL, sslmode='require')
  cursor = connection.cursor()
  cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
  # postgres_insert_query = """ INSERT INTO users variant VALUES %s"""
  # record_to_insert = 'One Plus 6'
  # cursor.execute(postgres_insert_query, record_to_insert)
  # connection.commit()
  # count = cursor.rowcount
  print ("Record inserted successfully into mobile table")

   # connection = psycopg2.connect(user="duozofkhzsfjvy",
   #                                password="46ef1e44c2b9751801126174b41e124a7f1c847b9e0cf2f27af49a0a3278d5db",
   #                                host="ec2-54-235-89-123.compute-1.amazonaws.com",
   #                                port="5432",
   #                                database="da1e3uq86ab5tu")
   # cursor = connection.cursor()

   # postgres_insert_query = """ INSERT INTO user (variant) VALUES (%s)"""
   # record_to_insert = ('One Plus 6')
   # cursor.execute(postgres_insert_query, record_to_insert)

   # connection.commit()
   # count = cursor.rowcount
   # print (count, "Record inserted successfully into mobile table")

except (Exception, psycopg2.Error) as error :
    print("Failed to insert record into mobile table", error)

finally:
    #closing database connection.
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")


