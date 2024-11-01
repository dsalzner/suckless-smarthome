#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""
from influx import action as influx_action
from shelly import action as shelly_action

if __name__ == "__main__":
    value = shelly_action('dishwasher-washingmaschine', "getpower")
    influx_action('dishwasher-washingmaschine_power', "addvalue", value)

