
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from urllib3 import Retry

# 配置 InfluxDB 客户端
token = ""
org = "mayInfluxDB"
url = "http://localhost:8086"
bucket = "symbol-bucket-200408"


# 创建 API 客户端和 InfluxDB 客户端
# api_client = ApiClient(url, token=token)
influx_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org,timeout = 120_000 , retries=Retry())

# influx_client = InfluxDBClient(url=url, token=token, org=org)

# 获取API实例



# 列出所有的保留策略
buckets_api = influx_client.buckets_api()


# influx_client.create_bucket(buckets_api)


policies = buckets_api.find_bucket_by_name(bucket)

print(policies)

buckets_api.delete_bucket(policies)
