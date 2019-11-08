import clickhouse
from clickhouse_driver import Client
client=Client(host='192.168.10.86',user='avx',password='ksMsw1w5fE',port='8123')

result = client.execute('show tables')

print(result)

