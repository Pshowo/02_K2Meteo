"""
Created on Apr 2020
MainProgram K2Meteo
@author: PawełJ
"""
import os
from apps import sqlite_db
import time
import pandas as pd

print('Welcome in K2Meteo, v0.1\n', '-'*50)

# SQLite========

# Create database if not exists
if not os.path.exists(sqlite_db.SQLITE_FILE):
    sqlite_db.db_create(sqlite_db.DB_PATH)
    conn = sqlite_db.db_connect(sqlite_db.DB_PATH)
    sqlite_db.db_create_default_tables(conn)
    sqlite_db.db_close(conn)

time_now = str(time.ctime(time.time()))
temp_current = 23
temp_min = 20.5
temp_max = 27.5

print("\nDate:\t\t\t\t", time_now,
      '\nCurrent temp:\t\t{}°C'.format(temp_current),
      '\nMin temperature:\t{}°C'.format(temp_min),
      '\nMax temperature:\t{}°C'.format(temp_max))

command = input("\nWrite 'read' to get max value from db:")
if command == "insert":
    insert_weather = (time_now, temp_current, temp_max, temp_min)
    conn = sqlite_db.db_connect(sqlite_db.DB_PATH)
    sqlite_db.db_insert_current_weather(conn, insert_weather)
    sqlite_db.db_close(conn)
    print("Add data to db.")

elif command == 'read':
    sql_get = """ SELECT MAX(TempMax) from current_weather """
    conn = sqlite_db.db_connect(sqlite_db.DB_PATH)
    sql_get_max1 = pd.read_sql_query(sql_get, conn)
    print("Max temperate in database is:\t{}°C".format(sql_get_max1['MAX(TempMax)'].iloc[0]))

# ========

