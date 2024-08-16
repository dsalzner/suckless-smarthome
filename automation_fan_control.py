#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""
from fritz_dect import action as dect_action
from philips_hue import action as hue_action

if __name__ == "__main__":
    temperature = dect_action("desk", "gettemperature")
    if float(temperature) > 26:
        hue_action("fan", "seton")
    else:
        hue_action("fan", "setoff")
