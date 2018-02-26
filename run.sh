#!/bin/sh
fuser -k -n tcp 8080
python setdata.py &
python control.py &
python pulldata.py &
python pulluser.py
