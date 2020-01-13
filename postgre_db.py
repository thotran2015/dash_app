import os
import psycopg2
try:
  DATABASE_URL = 'postgres://duozofkhzsfjvy:46ef1e44c2b9751801126174b41e124a7f1c847b9e0cf2f27af49a0a3278d5db@ec2-54-235-89-123.compute-1.amazonaws.com:5432/da1e3uq86ab5tu'

  connection = psycopg2.connect(DATABASE_URL, sslmode='require')
  cursor = connection.cursor()
  postgres_insert_query = """ INSERT INTO users variant VALUES %s"""
  record_to_insert = 'One Plus 6'
  cursor.execute(postgres_insert_query, record_to_insert)
  connection.commit()
  count = cursor.rowcount
  print (count, "Record inserted successfully into mobile table")

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
    #cursor.close()
        #connection.close()
        print("PostgreSQL connection is closed")


