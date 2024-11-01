#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""
from influx import action as influx_action
from fritz_dect import action as fritzdect_action

if __name__ == "__main__":
    try:
      value = fritzdect_action('desk', "gettemperature")
      influx_action('temp_desk', "addvalue", value)
    except:
      pass

    try:
      value = fritzdect_action('bedroom', "gettemperature")
      influx_action('temp_bedroom', "addvalue", value)
    except:
      pass

    try:
      value = fritzdect_action('livingroom', "gettemperature")
      influx_action('temp_livingroom', "addvalue", value)
    except:
      pass

