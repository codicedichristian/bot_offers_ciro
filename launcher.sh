#!/bin/bash

exec python3 -u main.py &
exec python3 -u amazon_bot/launcher.py
#lanciare il launcher.py con il loop invece di amazonMain.py
