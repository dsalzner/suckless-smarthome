## Suckless-Smarthome

Simple hassle-free Python scripts to control common smart home devices.

Build automations by simply importing the "action"-functions into your own scripts and running them from crontab.

Run them decentralized on your desktop computers, laptops, Android phone running Termux and Raspberry Pi home servers. 

No single points of failure.

The goal here is not to have extensive support for all features, but to have simple reusable scripts for the most common ones.

Each script is

* short
* handles one thing (separation of concerns)
* modular and reusable with a common interface
* runnable on command-line

### Usage

All scripts can be run on command-line and mostly use only two parameters ```--action``` and ```--device```.

They may return a single value depending on the action.

The scripts all have an ```def action(device, action):```-function in common. They may be imported to other Python scripts by use of that function.

#### Graphs

Suckless Smarthome supportes basic value storage and graphing. If you have an InfluxDB instance running you can build automations to add measurements and graph them.

##### InfluxDB

Configure InfluxDB access tokens in ```config.yml```:

```sh
influx_ip: <ip address of influxdb>
influx_db: <database name in influxdb>
```

Add a measuerment

```sh
python3 influx.py --action addvalue --device test --value 3
python3 influx.py --action addvalue --device test --value 4
python3 influx.py --action addvalue --device test --value 2
```

View measurements

```sh
python3 influx.py --action list --device test --duration 8h

{'time': '2024-08-16T13:24:01.560842Z', 'value': 3.0}, {'time': '2024-08-16T13:24:02.244833Z', 'value': 4.0}, {'time': '2024-08-16T13:24:02.617728Z', 'value': 2.0}]
```

##### Graph

With above InfluxDB configured.

Create a graph

```sh
python3 graph.py --action graph --device test --duration 8h
```

will produce a graph and store it as an *.png image

```
plot_test_8h.png
```

By copying that image onto a web server and making your own *.html-page you'll have a basic customizable smart home dashboard.

#### Automations

Suckless Smarthome makes it easy to build own custom automations by importing and using the ready-made modules in your own custom Python scripts.

##### Example: Store measurements to database

You can build simple automations, like adding measurements to the database by a script like this

```py
from influx import action as influx_action
from victron import action as victron_action

if __name__ == "__main__":
  for tag in ["batterycharge", "solarpower", "inverterpower", "batterycurrent"]:
    value = victron_action("", f'get{tag}')
    influx_action('photovoltaics-{tag}', "addvalue", value)
```

and adding it to cron

```
crontab -e
```

```
*/5  * * * * python3 automation_solar_to_db.py
```

##### Example: Control a fan depending on temperature

Or turn a fan on, when the temperature is above 26 degrees.

The fan can be connected to Philips Hue. The temperature can be received from a FritzDect plug.

```py
from fritz_dect import action as dect_action
from philips_hue import action as hue_action

if __name__ == "__main__":
  temperature = dect_action("desk", "gettemperature")
  if float(temperature) > 26:
    hue_action("fan", "seton")
  else:
    hue_action("fan", "setoff")
```

and adding that to cron

```
crontab -e
```

```
*/2  * * * * python3 automation_fan_control.py
```

#### Devices

Suckless Smarthome comes with a set of ready-made bindings. Feel free to adapt or add.

##### Philips Hue

Get a user token from Philips Hue device. Configure credendials in ```config.yml```:

```sh
philips_hue_ip: <ip address of hue bridge>
philips_hue_token: <user token of hue brige>
```

List devices

```sh
python3 philips_hue.py  --action list

Television
DiningTable
GardenPump
```

Get switch state

```sh         
python3 philips_hue.py --action getstate --device Television
```

Turn device on

```sh         
python3 philips_hue.py --action seton --device Television
```

or off

```sh
python3 philips_hue.py --action setoff --device Television
```

##### EspHome

Configure credendials in ```config.yml```:

```sh
esphome_<custom name for esphome device>_ip: <ip address of esp home>
esphome_<custom name for esphome device>_sensor: <name of the sensor to read from esphome device>
```

List devices

```sh
python3 esphome.py --action list

refridgerator-freezer
```

Read a value

```sh
python3 esphome.py --action getvalue --device refridgerator-freezer

10.9375
```

##### FritzDect

Configure credendials in ```config.yml```:

```sh
fritzdect_ip: <ip address of fritzbox>
fritzdect_user: <login username for fritzbox>
fritzdect_password: <login password for fritzbox>
```

List devices

```sh
python3 fritz_dect.py --action list

livingroom-socket
bedroom-heating
livingroom-heating
```

Get power reading

```sh
python3 fritz_dect.py --action getpower --device livingroom-socket

594.87
```

Get temperature reading

```sh
python3 fritz_dect.py --action gettemperature --device livingroom-socket

27.5
```

Get switch state

```sh
python3 fritz_dect.py --action getstate --device Steckdose2

1
```

Turn device on

```sh
python3 fritz_dect.py --action seton --device Steckdose2
```

or off

```sh
python3 fritz_dect.py --action setoff --device Steckdose2
```

##### Fritzbox

Configure credendials in ```config.yml```:

```sh
fritzbox_ip: <ip address of fritzbox>
fritzbox_user: <login username for fritzbox>
fritzbox_password: <login password for fritzbox>
```

```sh
python3 fritzbox.py --action gettotalbytessent
```

```sh
python3 fritzbox.py --action gettotalbytesreceived
```

```sh
python3 fritzbox.py --action getexternalipaddress
```

```sh
python3 fritzbox.py --action gettotalkilobytesreceived
```

```sh
python3 fritzbox.py --action gettotalkilobytessent
```

```sh
python3 fritzbox.py --action getupstreamutilization
```

```sh
python3 fritzbox.py --action getdownstreamutilization
```

##### Victron

Enable Mqtt on Victron OS device. Configure credendials in ```config.yml```:

```sh
victron_ip: <ip address of victron os device>
victron_id: <id of victron os device>
```

Get battery charge (Percentage)

```sh
python3 victron.py --action getbatterycharge
28.00
```

Get solar power input (Watt)

```sh
python3 victron.py --action getsolarpower
296.40
```

Get inverter Power (Volt-Ampere)

```sh
python3 victron.py --action getinverterpower
206.87
```

Get battery current flow (Ampere)

```sh
python3 victron.py --action getbatterycurrent
1.10
```

##### Yamaha AV-Receiver

Connect an ethernet cable to your AV-Receiver and enable Network standby. Configure credendials in ```config.yml```:

```sh
yamahaavr_ip: <ip address of AV Receiver>
```

Mute

```sh
python3 yamaha_avr.py --action mute
```

Unmute

```sh
python3 yamaha_avr.py --action unmute
```

On

```sh
python3 yamaha_avr.py --action on
```

Off

```sh
python3 yamaha_avr.py --action off
```


