#!/usr/bin/env python3

import sys
import time
import board
import Adafruit_DHT
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

sensor = 22 # adafruit_dht.DHT22
pin=4

# You can generate a Token from the "Tokens Tab" in the UI
token = "..."
org = "iot"
bucket = "iot"

client = InfluxDBClient(url="http://influx.matrix.lan:8086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
    try:
        humidity, temperature_c = Adafruit_DHT.read_retry(sensor, pin)

        point_1 = Point("temperature") \
          .tag("host", "zero1") \
          .field("temperature", temperature_c) \
          .time(datetime.utcnow(), WritePrecision.NS)

        point_2 = Point("humidity") \
          .tag("host", "zero1") \
          .field("humidity", humidity) \
          .time(datetime.utcnow(), WritePrecision.NS)

        write_api.write(bucket, org, point_1)
        write_api.write(bucket, org, point_2)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error) # .args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        raise error

    time.sleep(10.0)

