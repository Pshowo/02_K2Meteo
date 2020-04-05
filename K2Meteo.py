"""
Created on Apr 2020
MainProgram K2-Meteo
@author: PawełJ
"""
import os
from apps import sqlite_db
import time
import pandas as pd
import requests
import matplotlib.pyplot as plt
from matplotlib import ticker
import multiprocessing


def insert_temp_to_db(current_time, temp, temp_max, temp_min):
    insert_weather = (current_time, temp, temp_max, temp_min)
    conn_db = sqlite_db.db_connect(sqlite_db.DB_PATH)
    sqlite_db.db_insert_current_weather(conn_db, insert_weather)
    sqlite_db.db_close(conn_db)


def read_temp_db():
    sql_get = """ SELECT DateTime, Temp, TempMax, TempMin FROM current_weather """
    conn_db = sqlite_db.db_connect(sqlite_db.DB_PATH)
    sql_get_max1 = pd.read_sql_query(sql_get, conn_db)
    sqlite_db.db_close(conn_db)
    return sql_get_max1


# Max value =======================
def read_max_temp_db():
    sql_get = """ SELECT MAX(TempMax) from current_weather """
    conn_db = sqlite_db.db_connect(sqlite_db.DB_PATH)
    sql_get_max1 = pd.read_sql_query(sql_get, conn_db)
    sqlite_db.db_close(conn_db)
    print('-' * 50)
    print("  Max temperate in database is:\t{}°C".format(sql_get_max1['MAX(TempMax)'].iloc[0]))


# Current weather =======================
def print_weather(weather_url):
    time_now = str(time.ctime(time.time()))
    res_weather = requests.get(weather_url)
    data_weather = res_weather.json()

    temp_current = data_weather['main']['temp']
    temp_current_max = data_weather['main']['temp_max']
    temp_current_min = data_weather['main']['temp_min']
    desc_current = data_weather['weather'][0]['main']

    # Print current weather
    print('-' * 50, '\n   Current temperature on K2: {}\t'.format(time_now))
    print('\n   Current temp:\t{}°C'.format(temp_current),
          '\n   Max temperature:\t{}°C'.format(temp_current_max),
          '\n   Min temperature:\t{}°C'.format(temp_current_min),
          '\n   Actually weather:\t{}'.format(desc_current))


# Forecast weather =======================
def print_forecast(forecast_url):
    res_forecast = requests.get(forecast_url)
    data_forecast = res_forecast.json()
    print('-' * 50, '\n   Forecast weather in the next 5 days:')
    i = 1
    for day in data_forecast['list']:
        hour = day['dt_txt']
        if (hour[-8:]) == '12:00:00':
            desc_weather = day['weather'][0]['main']
            print("   Day {}:\t{}, \tTemp:{}, \tForecast weather: {}".format(i, day['dt_txt'], day['main']['temp'], desc_weather))
            i += 1


# Plot Graph =======================
def graph_plot():
    df_temp = read_temp_db()
    file_name = 'Temperature on K2 ' + str(time_now).replace(':', "_")
    y = df_temp['Temp'].astype(float)
    obj = df_temp['DateTime']

    fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)
    ax.plot(obj, y)
    ax.set(xlabel='Date & Time', ylabel='Temperature [°C]',
           title='Temperature on K2')

    ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
    plt.grid(True)
    plt.savefig(sqlite_db.SQLITE_PATH + "\\" + file_name)
    print('   You mast close the window with graph to continue.')
    plt.show()


def recording_data():
    while True:
        current_time = str(time.ctime(time.time()))
        data_weather = requests.get(weather).json()

        temp_current = data_weather['main']['temp']
        temp_current_max = data_weather['main']['temp_max']
        temp_current_min = data_weather['main']['temp_min']

        insert_temp_to_db(current_time, temp_current, temp_current_max, temp_current_min)
        time.sleep(30)


# UI ====================
def input_check():
    word = input('\n  Command:')
    word = word.lower()

    if word == 'weather':
        print_weather(weather)
        return input_check()
    elif word == 'forecast':
        print_forecast(forecast)
        time.sleep(1)
        print('   It\'s look so good. You can go to climbing.')
        time.sleep(1)
        print("   Probably.. :)")
        time.sleep(1)
        return input_check()
    elif word == 'max':
        read_max_temp_db()
        return input_check()
    elif word == 'graph':
        graph_plot()
        return input_check()
    elif word == 'exit':
        print('\n   Bye and good luck on climbing.')
        time.sleep(2)
        return ''
    elif word == 'help':

        print('-' * 50, '   \nYou can use this command:\n',
              '   "help" \t- Display available commands.\n',
              '   "weather"\t- Display current temperature on K2.\n',
              '   "forecast"\t- Display forecast weather in 5 days on K2.\n',
              '   "max"\t- Display max registered value on database.\n',
              '   "graph"\t- Plot graph and save picture on your disc.\n',
              '   "exit"\t- Close program.')
        return input_check()
    else:
        print("   We didn't understand your entry. Try again.")
        return input_check()


time_now = str(time.ctime(time.time()))
k2 = r"""
==============================================================================                                                                                              
  _  _____    __  __      _             
 | |/ /__ \  |  \/  |    | |            
 | ' /   ) | | \  / | ___| |_ ___  ___  
 |  <   / /  | |\/| |/ _ \ __/ _ \/ _ \ 
 | . \ / /_  | |  | |  __/ ||  __/ (_) |
 |_|\_\____| |_|  |_|\___|\__\___|\___/ 
                      _
                     /#\\
                    /###\     /\\
                   /  ###\   /##\  /\\
                  /      #\ /####\/##\\
                 /  /      /   # /  ##\             _       /\\
               // //  /\  /    _/  /  #\ _         /#\    _/##\    /\\
              // /   /  \     /   /    #\ \      _/###\_ /   ##\__/ _\\
             /  \   / .. \   / /   _   { \ \   _/       / //    /    \\
     /\     /    /\  ...  \_/   / / \   } \ | /  /\  \ /  _    /  /    \ /\\
/...\.../..:.\. ..:::::::..:..... . ...\{:... / %... \\/..%. \  /./:..\__   \\
..:..\:..:::....:::;;;;;;::::::::.:::::.\}.....::%.:. \ .:::. \/.%:::.:..\\;::
==============================================================================
"""

# SQLite ================
# Create database if not exists
if not os.path.exists(sqlite_db.DB_PATH):
    sqlite_db.db_create(sqlite_db.DB_PATH)
    conn = sqlite_db.db_connect(sqlite_db.DB_PATH)
    sqlite_db.db_create_default_tables(conn)
    sqlite_db.db_close(conn)

# Vaccum db
conn = sqlite_db.db_connect(sqlite_db.DB_PATH)
sqlite_db.db_vaccum(conn)
sqlite_db.db_close(conn)

# OpenWeatherMap ========
K2_CORD = {"lat": "35.88", "lon": "76.51"}
WODZISLAW = {"lat": "51.51", "lon": "-0.13"}
API = 'bc5101724fad77046c340e3c4706f87d'

weather = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}".format(K2_CORD['lat'], K2_CORD['lon'], API)
forecast = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units=metric&appid={}'.format(K2_CORD['lat'], K2_CORD['lon'], API)
time_now = str(time.ctime(time.time()))
res_weather = requests.get(weather)
data_weather = res_weather.json()

temp_current = data_weather['main']['temp']
temp_current_max = data_weather['main']['temp_max']
temp_current_min = data_weather['main']['temp_min']
desc_current = data_weather['weather'][0]['main']


'''
# Recording data ========
print("Recording data in process...")
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
    # print('Write Time:\t\t\t\t{}'.format(time_now),
    #       '\nCurrent temp:\t\t{}°C'.format(temp_current),
    #       '\nMax temperature:\t{}°C'.format(temp_current_max),
    #       '\nMin temperature:\t{}°C'.format(temp_current_min),)
    time.sleep(60)
'''


def main():
    print(k2)
    print('   Welcome in K2-Meteo, v1.0')
    print('   In this program you can use this command: "help", "weather", "forecast", "max", "graph" and "exit" ')
    print('  "If you forget the commands, write \"help\" in Command line."')

    print(os.getcwd())

    rec = multiprocessing.Process(target=recording_data)
    rec.start()
    print('  (Program in background is recording data to database.)')
    input_check()
    rec.terminate()
    rec.join()
    exit()


if __name__ == '__main__':
    main()
