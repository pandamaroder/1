from clickhouse_driver import Client
client=Client(host='192.168.10.86',user='avx',password='ksMsw1w5fE',port='9000')

client.execute("SELECT *  FROM schoolwifi_facts.device_handshake limit 1;")

from datetime import datetime, timedelta

import allure
import psycopg2
import pytest
from framework.resources.test_params.registration_data import TimepadLogin, TimepadEvent
from framework.ui_pages.registration_page import TimepadPage




hint_list = []

    # параметры подключения
pgsql_conf = "dbname='schoolwifi' user='postgres' password='postgres' host='192.168.10.68' port='5432'"
    #  подключение к БД
conn = psycopg2.connect(pgsql_conf)
cur = conn.cursor()

    # выбор города из БД
city_select = "SELECT * FROM schoolwifi.user_type"
cur.execute(city_select)
for row in cur:
    hint_list.append(row[1])
    print (hint_list)
conn.close()

print ('a')
print (hint_list)




hint_list = []

    # параметры подключения
pgsql_conf = "dbname='schoolwifi' user='postgres' password='postgres' host='192.168.10.68' port='5432'"
    #  подключение к БД
conn = psycopg2.connect(pgsql_conf)
cur = conn.cursor()

    # выбор города из БД
city_select = "SELECT * FROM schoolwifi.user_type"
cur.execute(city_select)
for row in cur:
    hint_list.append(row[1])
    print (hint_list)
conn.close()

print ('a')
print (hint_list)