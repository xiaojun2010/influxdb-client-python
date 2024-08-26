import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time
from urllib3 import Retry
import random
import datetime

token = ""
org = "mayInfluxDB"
url = "http://localhost:8086"
bucket = "symbol-bucket-200408"
# 字符串的格式
format_string = "%Y-%m-%d %H:%M:%S.%f"

symbol_list = []
i = 0
while i < 200 :
    symbol_list.append("BTC_USDT_{0}".format(i))
    i = i+1

source_list = ['OKX', 'BIAN', '', 'OKCOIN']

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org, timeout=120_000, retries=Retry())
write_api = client.write_api(write_options=SYNCHRONOUS)

date_string = "2024-08-26 20:24:08.191810"
datetime_object = datetime.datetime.strptime(date_string, format_string)

point_list = []
i = 0
max = 3000_000

# while i < max:
#     point = Point("symbol") \
#         .tag("symbol_id", random.choice(symbol_list)) \
#         .tag("source", random.choice(source_list)) \
#         .field("price", float(random.uniform(0, 1))) \
#         .time(time=datetime.datetime.now(tz=datetime.timezone.utc),
#               write_precision=WritePrecision.NS)  # 时间戳转换为毫秒 , precision=6 表示纳秒，即毫秒
#     point_list.append(point)
#     i = i + 1
#     if i % 1000 == 0:
#         write_api.write(bucket=bucket, org=org, record=point_list)
#         print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), " insert batch size = 1000 ")
#         point_list = []
#
# write_api.write(bucket=bucket, org=org, record=point_list)
# print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), " insert batch size = ", len(point_list))

# ' |> range(start: 0, stop: now())'

query = 'from(bucket:"' + bucket + '")' \
                                   ' |> range(start: -7d, stop: now())' \
                                   ' |> filter(fn: (r) => r._measurement == "symbol" )'
                                   # ' |> keep(columns: ["_time" ,"source" ,"symbol_id" ,"_field","_value","_measurement"])' \

# ' |> max()'

print( "query start :",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
tables = client.query_api().query(query, org=org)
print( "query end :",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))

print( "len(tables) = ",len(tables))
size = 0
for table in tables:
    size = size + len(table.records)

print("size = " ,size)


# for table in tables:
#     for record in table.records:
#         print(record)

# 删除
# start = datetime.datetime(1970, 1, 1, 0, 0, 0 ,0 , tzinfo=datetime.timezone.utc)
# stop = datetime.datetime(2025, 11, 10, 23, 0, 23 ,256 , tzinfo=datetime.timezone.utc)
# client.delete_api().delete(start, stop, '_measurement="symbol"', bucket=bucket, org=org)
# client.delete_api().delete(start, stop, '_measurement="financial-analysis"', bucket=bucket, org=org)


client.close()
