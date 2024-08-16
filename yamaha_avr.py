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
    url = f'http://{config["yamahaavr_ip"]:80/YamahaRemoteControl/ctrl'
    if action == "mute":
        data = '<YAMAHA_AV cmd="PUT"><Main_Zone><Volume><Mute>On</Mute></Volume></Main_Zone></YAMAHA_AV>'
    if action == "unmute":
        data = '<YAMAHA_AV cmd="PUT"><Main_Zone><Volume><Mute>Off</Mute></Volume></Main_Zone></YAMAHA_AV>'
    if action == "on":
        data = '<YAMAHA_AV cmd="PUT"><System><Power_Control><Power>On</Power></Power_Control></System></YAMAHA_AV>'
    if action == "off":
        data = '<YAMAHA_AV cmd="PUT"><System><Power_Control><Power>Standby</Power></Power_Control></System></YAMAHA_AV>'

    resp = requests.post(url=url, params=data)
    return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Yamaha AVR Binding',
        description='Yamaha AVR for Suckless SmartHome')
    parser.add_argument('-d', '--device')
    parser.add_argument('-a', '--action')
    args = parser.parse_args()
    print(action(args.device, args.action))
