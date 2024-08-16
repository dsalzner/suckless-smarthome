#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""
from influx import action as influx_action
from esphome import action as esphome_action

if __name__ == "__main__":
    value = esphome_action('fridge-cooler', "getvalue")
    influx_action('fridge-cooler', "addvalue", value)
