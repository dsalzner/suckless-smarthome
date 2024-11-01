#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""
from graph import action as graph_action
import glob
import os
import shutil

SCRIPT_DIR=os.path.dirname(os.path.realpath(__file__))

def graph_action_2(device, action, interval):
  try:
    graph_action(device, action, interval)
  except Exception as e:
    print(f'Err {device}: {e}')

if __name__ == "__main__":
    graph_action_2("fridge_cooler", "graph", "24h")
    graph_action_2("photovoltaics_solarpower", "graph", "24h")
    graph_action_2("photovoltaics_batterycharge", "graph", "24h")
    graph_action_2("photovoltaics_inverterpower", "graph", "24h")
    graph_action_2("dishwasher-washingmaschine_power", "graph", "24h")

    graph_action_2("temp_livingroom,temp_desk,temp_bedroom", "graph", "24h")

    graph_action_2("fridge_power", "graph", "24h")
    
    plants = [
      "soil_einblatt",
      "soil_a2",
      "soil_a3",
      "soil_b1",
      "soil_b2",
      "soil_b3",
      "soil_b4",
      "soil_b5"
    ]
    graph_action_2(",".join(plants), "graph", "24h")
    
    for img in glob.glob(os.path.join(SCRIPT_DIR, "plot_*.png")):
      shutil.copy(img, "/var/www/html/dashboard")
      
