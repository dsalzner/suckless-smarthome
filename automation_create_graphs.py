#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""
from graph import action as graph_action

if __name__ == "__main__":
    graph_action("fridge-cooler", "graph")
    graph_action("photovoltaics-solarpower", "graph")
    graph_action("photovoltaics-batterycharge", "graph")
