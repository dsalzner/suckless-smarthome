#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""

from influx import action as influx_action
from fritz_dect import action as fritzdect_action
from esphome import action as esphome_action

if __name__ == "__main__":
    value = fritzdect_action('fridge', 'getpower')
    influx_action('fridge_power', 'addvalue', value)

    value = esphome_action('fridge-cooler', 'getvalue')
    influx_action('fridge_cooler', 'addvalue', value)
