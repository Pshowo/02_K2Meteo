"""
Created on Apr 2020
Set of function to SQLite
@author: PawełJ
"""
import sqlite3
from sqlite3 import Error

SQLITE_FILE = 'k2_db.db'
SQLITE_PATH = r'D:\Python\08_K2Meteo\K2Meteo\Data'
DB_PATH = SQLITE_PATH + '/' + SQLITE_FILE


# Function to create database file
def db_create(file):
    conn = None
    try:
        conn = sqlite3.connect(file)
        print("Database created, SQLite version: ", sqlite3.version)
    except Error as er:
        print("db_create: ", er)
    finally:
        if conn:
            conn.close()


# Function to connect database
def db_connect(file):
    conn = None
    try:
        conn = sqlite3.connect(file)
        return conn
    except Error as er:
        print("Error db_connect: ", er)
    return conn


# Function to commit changes and close db
def db_close(conn):
    conn.commit()
    # Todo Dodać vaccum database
    conn.close()


# Function to create default tables on db
def db_create_default_tables(conn):
    if conn is not None:
        try:
            cur = conn.cursor()
        except Error as er:
            print("Error db_create_default_tables: ", er)
        else:
            sql_create_table_current_weather = """ CREATE TABLE IF NOT EXISTS current_weather (
                    DataId integer PRIMARY KEY,
                    DateTime text,
                    Temp real,
                    TempMax real,
                    TempMin real 
            );"""
            cur.execute(sql_create_table_current_weather)
    print("New table was created.")


# Function to add data into table current_weather
def db_insert_current_weather(conn, data):
    sql = """
        INSERT INTO current_weather (DateTime, Temp, TempMax, TempMin) VALUES (?, ?, ?, ?)
    """
    cur = conn.cursor()
    cur.execute(sql, data)
    return cur.lastrowid

