#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 22:49:06 2020

@author: thotran
"""
from constants import REDIS_URL, DATABASE_URL
import redis
import psycopg2

def set_redis(variant, data):
    conn = redis.from_url(REDIS_URL)
    conn.set(variant, data)
    conn.close()
    
def get_redis(variant):
    conn = redis.from_url(REDIS_URL)
    conn.close()
    return conn.get(variant)
    
def set_db(variant, data):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE TABLE variants (id serial PRIMARY KEY, data varchar);")
    except:
        print("I can't drop our test database!")

    conn.commit() # <--- makes sure the change is shown in the database

    #Closing the connection
    conn.close()
    
    
def get_db(variant):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    command = 'SELECT id, data FROM variants WHERE id = ' + str(variant)
    data = cursor.execute(command)
    conn.close()
    return data
