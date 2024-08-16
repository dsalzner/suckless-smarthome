#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""

import argparse
import requests
from requests.auth import HTTPDigestAuth
import yaml
import xmltodict

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

def _get(service_type, control_url, field_1, field_2):
    url = f'http://{config["fritzbox_ip"]}:49000/{control_url}' 
    headers={
        'Content-Type': 'text/xml; charset=utf-8',
        'SoapAction': f'{service_type}#{field_1}'
    }
    data = f'<?xml version="1.0" encoding="utf-8"?> <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"> <s:Body> <u:{field_1} xmlns:u="{service_type}" /> </s:Body> </s:Envelope>'
    auth = HTTPDigestAuth(config["fritzbox_user"], config["fritzbox_password"])
    response = requests.post(url=url, data=data, auth=auth, headers=headers)
    d = xmltodict.parse(response.text)
    return d["s:Envelope"]["s:Body"]["u:" + field_1 + "Response"][field_2]

def action(device, action):
    service_type = "urn:schemas-upnp-org:service:WANIPConnection:1"
    control_url = "igdupnp/control/WANIPConn1"
    if action == "getexternalipaddress":
        return _get(
            service_type,
            control_url,
            "GetExternalIPAddress",
            "NewExternalIPAddress",
        )

    service_type = "urn:dslforum-org:service:WANCommonInterfaceConfig:1"
    control_url = "upnp/control/wancommonifconfig1"
    
    if action == "gettotalbytessent":
        return _get(
            service_type,
            control_url,
            "GetTotalBytesSent",
            "NewTotalBytesSent",
        )
    if action == "gettotalbytesreceived":
        return _get(
            service_type,
            control_url,
            "GetTotalBytesReceived",
            "NewTotalBytesReceived",
        )
        
    if action == "gettotalkilobytessent":
        return _get(
            service_type,
            control_url,
            "GetTotalBytesSent",
            "NewTotalBytesSent",
        )
    if action == "gettotalkilobytesreceived":
        return _get(
            service_type,
            control_url,
            "GetTotalBytesReceived",
            "NewTotalBytesReceived",
        )
        
    service_type = "urn:dslforum-org:service:WANCommonInterfaceConfig:1"
    control_url = "upnp/control/wancommonifconfig1"
    
    if action == "getupstreamutilization":
        return _get(
            service_type,
            control_url,
            "GetCommonLinkProperties",
            "NewX_AVM-DE_UpstreamCurrentUtilization",
        )
        
    if action == "getdownstreamutilization":
        return _get(
            service_type,
            control_url,
            "GetCommonLinkProperties",
            "NewX_AVM-DE_DownstreamCurrentUtilization",
        )
        
    return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Fritzbox Binding',
        description='Fritzbox for Suckless SmartHome')
    parser.add_argument('-d', '--device')
    parser.add_argument('-a', '--action')
    args = parser.parse_args()
    print(action(args.device, args.action))
