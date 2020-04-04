"""
Created on Apr 2020
MainProgram K2Meteo
@author: PawełJ
"""
import os
from apps import sqlite_db
import time
import pandas as pd
import requests

print('Welcome in K2Meteo, v0.2\n', '-'*50)

# SQLite ================

# Create database if not exists
if not os.path.exists(sqlite_db.DB_PATH):
    sqlite_db.db_create(sqlite_db.DB_PATH)
    conn = sqlite_db.db_connect(sqlite_db.DB_PATH)
    sqlite_db.db_create_default_tables(conn)
    sqlite_db.db_close(conn)

time_now = str(time.ctime(time.time()))

command = ''


# command = input("\nWrite 'read' to get max value from db:")
def insert_temp_to_db(time_now, temp_current, temp_max, temp_min):
    insert_weather = (time_now, temp_current, temp_max, temp_min)
    conn = sqlite_db.db_connect(sqlite_db.DB_PATH)
    sqlite_db.db_insert_current_weather(conn, insert_weather)
    sqlite_db.db_close(conn)


if command == 'read':
    sql_get = """ SELECT MAX(TempMax) from current_weather """
    conn = sqlite_db.db_connect(sqlite_db.DB_PATH)
    sql_get_max1 = pd.read_sql_query(sql_get, conn)
    print("Max temperate in database is:\t{}°C".format(sql_get_max1['MAX(TempMax)'].iloc[0]))

# =======================

# OpenWeatherMap ========
K2_CORD = {"lat": "35.88", "lon": "76.51"}
WODZISLAW = {"lat": "51.51", "lon": "-0.13"}
API = 'bc5101724fad77046c340e3c4706f87d'

weather_url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}".format(
    WODZISLAW['lat'], WODZISLAW['lon'], API)
forecast = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units=metric&appid={}'.format(K2_CORD['lat'],
                                                                                                         K2_CORD['lon'],
                                                                                                         API)
while True:
    time_now = str(time.ctime(time.time()))
    res_weather = requests.get(weather_url)
    res_forecast = requests.get(forecast)
    data_weather = res_weather.json()
    data_forecast = res_forecast.json()

    temp_current = data_weather['main']['temp']
    temp_current_max = data_weather['main']['temp_max']
    temp_current_min = data_weather['main']['temp_min']
    desc_current = data_weather['weather'][0]['main']

    insert_temp_to_db(time_now, temp_current, temp_current_max, temp_current_min)

    # Current weather
    print('-' * 50, '\nCurrent temperature in K2:')
    print('Time:\t\t\t\t{}'.format(time_now),
          '\nCurrent temp:\t\t{}°C'.format(temp_current),
          '\nMax temperature:\t{}°C'.format(temp_current_max),
          '\nMin temperature:\t{}°C'.format(temp_current_min),
          '\nActually weather:\t{}'.format(desc_current))
    time.sleep(60)


# Forecast weather
print('-' * 50, '\nForecast weather in the next 5 days:')
i = 1
for day in data_forecast['list']:
    hour = day['dt_txt']
    if (hour[-8:]) == '12:00:00':
        desc_weather = day['weather'][0]['main']
        print("Day {}:\t{}, \tTemp:{}, \tForecast weather: {}".format(i, day['dt_txt'], day['main']['temp'],
                                                                      desc_weather))
        i += 1

# =======================
