#!/bin/bash
cd /home/codered/smarthome/ # && ./automation_*.py

for f in automation_*.py; do
   python3 "$f" 
done

