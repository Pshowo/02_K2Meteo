"""
Created on Apr 2020
MainProgram K2Meteo
@author: PawełJ
"""
import os
from apps import sqlite_db

print('Welcome in K2Meteo, v0.1\n', '-'*50)

# Create database if not exists
if not os.path.exists(sqlite_db.SQLITE_FILE):
    sqlite_db.db_create(sqlite_db.DB_PATH)
    conn = sqlite_db.db_connect(sqlite_db.DB_PATH)
    sqlite_db.db_create_default_tables(conn)
    sqlite_db.db_close(conn)



