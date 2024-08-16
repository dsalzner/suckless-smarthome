#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""

import argparse
import json
import paho.mqtt.client as mqtt # pip install paho-mqtt
import requests
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

tag = ""
value = ""

topics = {
    "batterycharge" : f'N/{config["victron_id"]}/system/0/Dc/Battery/Soc',
    "solarpower" : f'N/{config["victron_id"]}/system/0/Dc/Pv/Power',
    "inverterpower" : f'N/{config["victron_id"]}/system/0/Ac/Consumption/L1/Power',
    "batterycurrent" : f'N/{config["victron_id"]}/system/0/Dc/Battery/Current'
}

def _on_connect(client, userdata, flags, rc, properties):
    client.subscribe(topics[tag])

def _on_message(client, userdata, msg):
    global value
    value = json.loads(msg.payload)["value"]
    if msg.topic == topics[tag]:
        value ="{:.2f}".format(float(value))

def _get():
    global value
    value = ""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = _on_connect
    client.on_message = _on_message
    client.connect(config["victron_ip"], 1883, 60)
    ret= client.publish(f'R/{config["victron_id"]}/keepalive',"")
    while value == "":
        client.loop()
    return value

def action(device, action):
    global tag
    tag = action.replace("get", "")
    return _get()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Victron Binding',
        description='Victron for Suckless SmartHome')
    parser.add_argument('-d', '--device')
    parser.add_argument('-a', '--action')
    args = parser.parse_args()
    print(action(args.device, args.action))
