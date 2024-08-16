#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""

import argparse
import hashlib
import requests
import xmltodict
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

def _challengeResponse():
    # -- get challenge
    r = requests.get(f'http://{config["fritzdect_ip"]}/login_sid.lua')
    dict_data = xmltodict.parse(r.content)
    challenge = dict_data["SessionInfo"]["Challenge"]

    # -- post response
    response = hashlib.md5(f'{challenge}-{config["fritzdect_password"]}'.encode('utf-16le')).hexdigest()

    # -- get session id
    r = requests.get(f'http://{config["fritzdect_ip"]}/login_sid.lua', params = {
        "username": config["fritzdect_user"],
        "response": f"{challenge}-{response}"
    })
    dict_data = xmltodict.parse(r.content)
    sid = dict_data["SessionInfo"]["SID"]

    return sid

def _getDeviceList():
    sid = _challengeResponse()
    response = requests.get(f'http://{config["fritzdect_ip"]}/webservices/homeautoswitch.lua?sid={sid}&switchcmd=getdevicelistinfos')
    data = xmltodict.parse(response.content)
    return data

def action(device, action):
    if action == "list":
        for device_info in _getDeviceList()["devicelist"]["device"]:
            print(device_info["name"])
        return ""

    for device_info in _getDeviceList()["devicelist"]["device"]:
        if device_info["name"] == device:
            data = device_info

    if action == "getpower":
        return float(data["powermeter"]["power"])/1000
    if action == "gettemperature":
        return float(data["temperature"]["celsius"])/10
    if action == "getstate":
        return data["switch"]["state"]

    product = data["@productname"][-3:][:-1]
    ain = data["@identifier"].replace(" ", "%" + product)
    sid = _challengeResponse()
    url = f'http://{config["fritzdect_ip"]}/webservices/homeautoswitch.lua?ain={ain}&sid={sid}&switchcmd=setsimpleonoff&onoff='

    if action == "setoff":
        requests.get(f'{url}0')
    if action == "seton":
        requests.get(f'{url}1')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='FritzDect Binding',
        description='FritzDect for Suckless SmartHome')
    parser.add_argument('-d', '--device')
    parser.add_argument('-a', '--action')
    args = parser.parse_args()
    print(action(args.device, args.action))
