#!/bin/sh
# realiza las cargas de datos necesarias previas a ejecutar:
# $ python scheduler.py en modo simulación

python load_overshooters.py
python load_rets.py
python load_terrains.py
