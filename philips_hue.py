#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""

import argparse
from collections import defaultdict
import json
import requests
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

def _getDeviceList():
    response = requests.get(f'http://{config["philips_hue_ip"]}/api/{config["philips_hue_token"]}/lights/')
    data = json.loads(response.text)
    devices = defaultdict(lambda: '')
    for idx in data.keys():
        device = data[idx]["name"]
        devices[device] = idx
    return devices

def action(device, action):
    devices = _getDeviceList()

    if action == "list":
        for name in devices.keys():
            print(name)
        return ""

    if action == "getstate":
        response = requests.get(f'http://{config["philips_hue_ip"]}/api/{config["philips_hue_token"]}/lights/')
        data = json.loads(response.text)
        if data[devices[device]]["state"]["on"] == False:
            return "0"
        else:
            return "1"

    url = f'http://{config["philips_hue_ip"]}/api/{config["philips_hue_token"]}/lights/{devices[device]}/state'
    if action == "seton":
        requests.put(url, data = "{\"on\":true}")
    if action == "setoff":
        requests.put(url, data = "{\"on\":false}")

    return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Philips Hue Binding',
        description='Philips Hue Binding for Suckless SmartHome')
    parser.add_argument('-d', '--device')
    parser.add_argument('-a', '--action')
    args = parser.parse_args()
    print(action(args.device, args.action))
