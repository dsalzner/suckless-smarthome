#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""

from influx import action as influx_action
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import os
import yaml

SCRIPT_DIR=os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(SCRIPT_DIR, 'config.yml'), 'r') as file:
    config = yaml.safe_load(file)

def action(devices, action, duration='12h'):
    if action == "graph":
        ax = None
        plt.rcParams["figure.figsize"] = (5,3)
        plt.rcParams['lines.linewidth'] = 2

        for device in devices.split(","):
            try:            
                entries = influx_action(device, "list", duration=duration)
            except:
                print("err2")
                continue
            df = pd.DataFrame(entries)
            try:
                 df.set_index('time', inplace = True)
                 df.index = pd.to_datetime(df.index, utc=True).map(lambda x: x.tz_convert(config["graph_timezone"]))
            except:
                 print("err3")
                 continue
            if ax is None:
                ax = df.plot()
            else:
                df.plot(ax=ax)

        ax.yaxis.tick_right()

        plt.subplots_adjust(left=0.04, right=0.92, top=0.99, bottom=0.2)
        plt.savefig(f'plot_{"-".join(devices.split(","))}_{duration}.png', transparent=True)
    return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Graph Binding',
        description='Graph for Suckless SmartHome')
    parser.add_argument('-d', '--devices')
    parser.add_argument('-a', '--action')
    parser.add_argument('-t', '--duration', default='12h')
    args = parser.parse_args()
    print(action(args.devices, args.action, args.duration))
