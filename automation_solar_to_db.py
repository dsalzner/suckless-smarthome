#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""
from influx import action as influx_action
from victron import action as victron_action

if __name__ == "__main__":
    for tag in ["batterycharge", "solarpower", "inverterpower", "batterycurrent"]:
        value = victron_action("", f'get{tag}')
        influx_action('photovoltaics-{tag}', "addvalue", value)