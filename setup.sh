#!/bin/bash

if [ ! -d /home/claker/code/MemeKingBot/venv ]; then
  pythom -m venv venv
fi

source /home/claker/code/MemeKingBot/venv/bin/activate

pip install -r requirements.txt
