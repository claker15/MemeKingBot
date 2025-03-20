#!/bin/bash

if [ ! -d venv ]; then
  pythom -m venv venv
fi

source venv/bin/activate

pip install -r requirements.txt

python bot/bot.py