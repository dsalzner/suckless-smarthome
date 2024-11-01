#!/usr/bin/python3
"""
Suckless Smarthome
2024 D.Salzner <mail@dennissalzner.de>
"""
import time
from philips_hue import action as hue_action
from yamaha_avr import action as avr_action

if hue_action("Fernseher", "getstate") == 0:
    hue_action("Fernseher", "seton")
    time.sleep(15) # time for av reciever to turn on

avr_action("", "on")
time.sleep(1)
avr_action("", "volume_50")

for i in range(0,3):
    time.sleep(1)
    avr_action("", "back")

time.sleep(1)
avr_action("", "net_radio")

time.sleep(1)
avr_action("", "select_2") # "My Stations"
time.sleep(1)
avr_action("", "select_1") # "Unsere"
time.sleep(1)
avr_action("", "select_1") # "Serenade Radio"
