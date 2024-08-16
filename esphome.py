#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""

import argparse
import requests
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

def action(device, action):
    if action == "list":
        for key in config.keys():
            if key.startswith("esphome_") and key.endswith("_ip"):
                print(key.replace("esphome_", "").replace("_ip", ""))
        return ""

    if action == "getvalue":
        url = f'http://{config["esphome_" + device + "_ip"]}/sensor/{config["esphome_" + device + "_sensor"]}'
        resp = requests.get(url=url, params={})
        return resp.json()["value"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='EspHome Binding',
        description='EspHome for Suckless SmartHome')
    parser.add_argument('-d', '--device')
    parser.add_argument('-a', '--action')
    args = parser.parse_args()
    print(action(args.device, args.action))
