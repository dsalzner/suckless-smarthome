#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""
from influxdb import InfluxDBClient
import argparse
import os
import requests
import yaml

SCRIPT_DIR=os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(SCRIPT_DIR, 'config.yml'), 'r') as file:
    config = yaml.safe_load(file)

client = InfluxDBClient(config["influx_ip"], 8086, 'root', 'root', config["influx_db"])

def _add(measurement, value):
    data = [
        {"measurement" : measurement,
            "fields": {
                "value": float(value)
            }             
        }
    ]
    client.create_database(config["influx_db"])
    client.write_points(data)

def _list(device, duration):
    query = f'select * from "{device}" where time>now()-{duration};'
    records = client.query(query)
    entries = []
    for k, v in records.items():
        for p in v:
                data = {'time': p['time'], device: p['value']}
                entries += [data]
    return entries

def action(device, action, value="", duration="12h"):
    if action == "list":
        return _list(device, duration)
 
    if action == "addvalue":
        _add(device, value)

    return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='InfluxDB Binding',
        description='InfluxDB for Suckless SmartHome')
    parser.add_argument('-d', '--device')
    parser.add_argument('-a', '--action')
    parser.add_argument('-v', '--value')
    parser.add_argument('-t', '--duration')
    args = parser.parse_args()
    print(action(args.device, args.action, args.value, args.duration))
