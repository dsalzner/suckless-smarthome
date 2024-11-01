#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""
import argparse
import os
import requests
import yaml

SCRIPT_DIR=os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(SCRIPT_DIR, 'config.yml'), 'r') as file:
    config = yaml.safe_load(file)

def action(device, action):
    if action == "list":
        for key in config.keys():
            if key.startswith("shelly_") and key.endswith("_ip"):
                print(key.replace("shelly_", "").replace("_ip", ""))
        return ""

    if action == "getpower":
        url = f'http://{config["shelly_" + device + "_ip"]}/rpc/Switch.GetStatus?id=0'
        resp = requests.get(url=url, params={})
        return resp.json()["apower"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Shelly Binding',
        description='Shelly for Suckless SmartHome')
    parser.add_argument('-d', '--device')
    parser.add_argument('-a', '--action')
    args = parser.parse_args()
    print(action(args.device, args.action))
