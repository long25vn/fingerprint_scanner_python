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

#####connectDatabase####################################################
conn = psycopg2.connect(database="postgres", user = "postgres", password = "123", host = "127.0.0.1", port = "6000")
cur = conn.cursor()

print "Opened database successfully"
#####connectDevice####################################################
# zk = zklib.ZKLib("192.168.1.201", 4370)
# ret = zk.connect()
# sys.path.append("zk")
# zkteco = None
# zkteco = ZK('192.168.1.201', port=4370, timeout=5)
# zkteco = zkteco.connect()
# print "connection to device:", ret

# #####clearUser####################################################
# zk.clearUser()
#########################################################
tempstr1 = '2018-02-28'
tempstr2 = '2018-02-22'
tempstr3 = '2018-02-24'
tempstr4 = '2018-02-26'
tempint = 1
hela1 = time(10,00,00)
hela2 = time(00,45,00)
hela3 = time(18,00,00)
hela5 = time(9,00,00)
hela6 = time(00,00,00)
hela7 = time(9,20,00)
hela8 = time(00,5,00)
hela9 = time(9,30,00)
hela10 = time(00,15,00)
password = '123456'
cur.execute("DELETE from usertable;") 
cur.execute("INSERT INTO usertable (uid,id,name,privilege) VALUES  (" + str(1) + "," + str(1) + "," + `str("Halo")` + "," + `str("User")` + ")" )
cur.execute("INSERT INTO usertable (uid,id,name,privilege) VALUES  (" + str(2) + "," + str(2) + "," + `str("Gengi")` + "," + `str("User")` + ")" )
cur.execute("INSERT INTO usertable (uid,id,name,privilege) VALUES  (" + str(3) + "," + str(3) + "," + `str("Antonio")` + "," + `str("User")` + ")" )
cur.execute("INSERT INTO usertable (uid,id,name,privilege) VALUES  (" + str(4) + "," + str(4) + "," + `str("Fermen")` + "," + `str("User")` + ")" )
print str("Done")
cur.execute("INSERT INTO datatable (id,name,DATE,point,timein,timeout,STATE,timelate) VALUES ("+  str(1) + ",'" + str('Halo') + "'," + `tempstr3` + "," + `1` +"," + `str(hela1)` + "," +`str(hela3)` + "," + `1`+ "," + `str(hela2)` + ")" )
cur.execute("INSERT INTO datatable (id,name,DATE,point,timein,timeout,STATE,timelate) VALUES ("+  str(2) + ",'" + str('Gengi') + "'," + `tempstr3` + "," + `1` +"," + `str(hela1)` + "," +`str(hela3)` + "," + `1`+ "," + `str(hela2)` + ")" )
cur.execute("INSERT INTO datatable (id,name,DATE,point,timein,timeout,STATE,timelate) VALUES ("+  str(1) + ",'" + str('Halo') + "'," + `tempstr1` + "," + `1000` +"," + `str(hela7)` + "," +`str(hela3)` + "," + `1`+ "," + `str(hela8)` + ")" )
cur.execute("INSERT INTO datatable (id,name,DATE,point,timein,timeout,STATE,timelate) VALUES ("+  str(2) + ",'" + str('Gengi') + "'," + `tempstr1` + "," + `1000` +"," + `str(hela1)` + "," +`str(hela3)` + "," + `1`+ "," + `str(hela2)` + ")" )
cur.execute("INSERT INTO datatable (id,name,DATE,point,timein,timeout,STATE,timelate) VALUES ("+  str(4) + ",'" + str('Fermen') + "'," + `tempstr4` + "," + `1000000` +"," + `str(hela1)` + "," +`str(hela3)` + "," + `1`+ "," + `str(hela2)` + ")" )
conn.commit()  
