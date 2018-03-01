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

    y = []
    z = []
    g = []

    ########## connect to device #########
    zk = zklib.ZKLib("192.168.1.201", 4370)
    ret = zk.connect()
    sys.path.append("zk")
    zkteco = None
    zkteco = ZK('192.168.1.201', port=4370, timeout=5)
    zkteco = zkteco.connect()
    print "connection to device:", ret
    data_user = zk.getUser()
    zkteco_users = zkteco.get_users()
    attendance = zk.getAttendance()


    if ( attendance ):
        for lattendance in attendance:
                for uid in data_user:
                    if int(data_user[uid][0]) == int(lattendance[0]):
                        timerequest = datetime.combine(date.min, lattendance[2].time())
                        timein = datetime.combine(date.min, datetime.time(datetime.strptime('09:00:00', '%H:%M:%S')))
                        timedefault1 = datetime.combine(date.min, datetime.time(datetime.strptime('09:00:00', '%H:%M:%S')))
                        timedefault2 = datetime.combine(date.min, datetime.time(datetime.strptime('11:45:00', '%H:%M:%S')))
                        timedefault3 = datetime.combine(date.min, datetime.time(datetime.strptime('14:00:00', '%H:%M:%S')))
                        timedefault4 = datetime.combine(date.min, datetime.time(datetime.strptime('17:45:00', '%H:%M:%S')))
                        timedefault5 = datetime.combine(date.min, datetime.time(datetime.strptime('03:00:00', '%H:%M:%S')))
                        timedefault6 = datetime.combine(date.min, datetime.time(datetime.strptime('08:00:00', '%H:%M:%S')))
                        timelate = datetime.time(datetime.strptime('00:00:00', '%H:%M:%S'))
                        if (timedefault1 < timerequest < timedefault2):
                            timelate = timerequest - timedefault1
                        elif (timedefault3 < timerequest < timedefault4):
                            timelate = timerequest - timedefault3

                        cur.execute("SELECT id,timein,timeout from datatable WHERE (id,date) = " + "(" + `lattendance[0]` + "," + `str(lattendance[2].date())` + ")" )
                        rowss = cur.fetchall() 
                        if (rowss != []):
                            halftime = time(03,00,00)
                            fulltime = time(8,00,00)    
                            timesub = timerequest - datetime.combine(date.min, rowss[0][1])
                            f = (datetime.min + timesub).time()
                            point = 1
                            if f >= fulltime:
                                point = 100
                            elif fulltime > f >= halftime:
                                point = 10
                            cur.execute("UPDATE datatable set (point,timeout) = (" +  `point` + "," + `str(timerequest)` + ") where (id,date) = " + "(" + `lattendance[0]` + "," + `str(lattendance[2].date())` + ")" )
                            conn.commit()    
                            zk.clearAttendance()
                        elif (rowss == []):   
                            cur.execute("SELECT numerical from datatable WHERE numerical=(select max(numerical) from datatable)")
                            rows = cur.fetchall()
                            numerical =  int(rows[0][0]) + 1
                            cur.execute("INSERT INTO datatable (numerical,id,name,DATE,point,timein,STATE,timelate) VALUES \
                            ("+  `numerical` + "," +  `lattendance[0]` + "," + `data_user[uid][1]` + "," + `str(lattendance[2].date())` + "," + `1` + ","+ \
                            `str(timerequest)` + "," + `str(lattendance[1])` + "," + `str(timelate)` +")")
                            conn.commit()
                            zk.clearAttendance()
    print ("jnla")
    sleep (5)
