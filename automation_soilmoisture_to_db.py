#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""
from influx import action as influx_action
from esphome import action as esphome_action

if __name__ == "__main__":
    plants = [
      ("soilmoisture-a1", "soil_einblatt"),
      ("soilmoisture-a2", "soil_a2"),
      ("soilmoisture-a3", "soil_a3"),
      ("soilmoisture-b1", "soil_b1"),
      ("soilmoisture-b2", "soil_b2"),
      ("soilmoisture-b3", "soil_b3"),
      ("soilmoisture-b4", "soil_b4"),
      ("soilmoisture-b5", "soil_b5"),
    ]
    for (id, name) in plants:
      value = esphome_action(id, "getvalue")
      print(f'{name}: {value}')
      influx_action(name, "addvalue", value)
