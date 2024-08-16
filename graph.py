#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""

from influx import action as influx_action
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def action(device, action, duration="12h"):
    if action == "graph":
        entries = influx_action(device, "list", duration)
        df = pd.DataFrame(entries)
        df.set_index('time', inplace = True)
        df.index = pd.to_datetime(df.index)
        df.plot()
        plt.savefig(f'plot_{device}_{duration}.png')
    return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Graph Binding',
        description='Graph for Suckless SmartHome')
    parser.add_argument('-d', '--device')
    parser.add_argument('-a', '--action')
    parser.add_argument('-t', '--duration')
    args = parser.parse_args()
    print(action(args.device, args.action, args.duration))
