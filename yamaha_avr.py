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
    headers = {'Content-Type': 'text/xml'}
    data = '<?xml version="1.0" encoding="utf-8"?>'
    url = f'http://{config["yamahaavr_ip"]}/YamahaRemoteControl/ctrl'
    if action == "mute":
        data += '<YAMAHA_AV cmd="PUT"><Main_Zone><Volume><Mute>On</Mute></Volume></Main_Zone></YAMAHA_AV>'
    if action == "unmute":
        data += '<YAMAHA_AV cmd="PUT"><Main_Zone><Volume><Mute>Off</Mute></Volume></Main_Zone></YAMAHA_AV>'
    if action == "on":
        data += '<YAMAHA_AV cmd="PUT"><System><Power_Control><Power>On</Power></Power_Control></System></YAMAHA_AV>'
    if action == "off":
        data += '<YAMAHA_AV cmd="PUT"><System><Power_Control><Power>Standby</Power></Power_Control></System></YAMAHA_AV>'

    # -- switch to net radio --
    if action == "net_radio":
        data += '<YAMAHA_AV cmd="PUT"><Main_Zone><Input><Input_Sel>NET RADIO</Input_Sel></Input></Main_Zone></YAMAHA_AV>'

    # -- cursor control --
    if action == "back":
        data += '<YAMAHA_AV cmd="PUT"><NET_RADIO><List_Control><Cursor>Back</Cursor></List_Control></NET_RADIO></YAMAHA_AV>'
    if action == "select_1":
        data += '<YAMAHA_AV cmd="PUT"><NET_RADIO><List_Control><Direct_Sel>Line_1</Direct_Sel></List_Control></NET_RADIO></YAMAHA_AV>'
    if action == "select_2":
        data += '<YAMAHA_AV cmd="PUT"><NET_RADIO><List_Control><Direct_Sel>Line_2</Direct_Sel></List_Control></NET_RADIO></YAMAHA_AV>'
    
    if action == "volume_50":
        data += '<YAMAHA_AV cmd="PUT"><Main_Zone><Volume><Lvl><Val>-500</Val><Exp>1</Exp><Unit>dB</Unit></Lvl></Volume></Main_Zone></YAMAHA_AV>'

    print(url)
    print(data)

    print(requests.post(url=url, data=data, headers=headers).text)
    return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Yamaha AVR Binding',
        description='Yamaha AVR for Suckless SmartHome')
    parser.add_argument('-d', '--device')
    parser.add_argument('-a', '--action')
    args = parser.parse_args()
    print(action(args.device, args.action))
