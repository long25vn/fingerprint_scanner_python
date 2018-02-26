#!/bin/sh
python setdata.py &
python control.py &
python pushdata.py
