#!/bin/bash

mkdir log
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
nohup python meal_bot.py &
echo $! >> meal-bot.pid