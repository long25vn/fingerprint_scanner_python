import sys
import json
sys.path.append("zklib")
from zklib import zklib
from zk import ZK, const

import time
import zkconst
from time import sleep
from flask import Flask, flash, redirect, render_template, request, session, abort
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
from datetime import datetime, date, time
import psycopg2

while True:
    conn = psycopg2.connect(database="postgres", user = "postgres", password = "123", host = "127.0.0.1", port = "6000")
    cur = conn.cursor()
    print "Opened database successfully"

    ########## connect to device #########
    zk = zklib.ZKLib("192.168.1.201", 4370)
    ret = zk.connect()
    if ret == True:
        print "connected to device"
        sys.path.append("zk")
        zkteco = None
        zkteco = ZK('192.168.1.201', port=4370, timeout=5)
        zkteco = zkteco.connect()
        data_user = zk.getUser()
        zkteco_users = zkteco.get_users()
        cur.execute("DELETE from usertable;") 

        for user in zkteco_users:
            privilege = 'User'
            if user.privilege == const.USER_ADMIN:
                privilege = 'Admin'
            uid = format(user.uid)
            name = format(user.name)
            privilege = format(privilege)
            password = format(user.password)
            group = format(user.group_id)
            id = format(user.user_id)
            cur.execute("INSERT INTO usertable (uid,id,name,privilege) VALUES  (" + str(uid) + "," + str(id) + "," + `str(name)` + "," + `str(privilege)` + ")" )
            conn.commit()
        print ("done")
        sleep (3)
    else:
        print "Device Disconect"