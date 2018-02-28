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
conn = psycopg2.connect(database="postgres", user = "postgres", password = "123", host = "127.0.0.1", port = "5432")
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
cur.execute("DELETE from datatable;") 
cur.execute("INSERT INTO usertable (uid,id,name,privilege) VALUES  (" + str(1) + "," + str(1) + "," + `str("Halo")` + "," + `str("User")` + ")" )
cur.execute("INSERT INTO usertable (uid,id,name,privilege) VALUES  (" + str(2) + "," + str(2) + "," + `str("Gengi")` + "," + `str("User")` + ")" )
cur.execute("INSERT INTO usertable (uid,id,name,privilege) VALUES  (" + str(3) + "," + str(3) + "," + `str("Antonio")` + "," + `str("User")` + ")" )
cur.execute("INSERT INTO usertable (uid,id,name,privilege) VALUES  (" + str(4) + "," + str(4) + "," + `str("Fermen")` + "," + `str("User")` + ")" )
# zkteco.set_user(uid=int(1), name=str("Halo"), privilege=const.USER_DEFAULT, password=str(password), group_id='', user_id=str(1))
# zkteco.set_user(uid=int(2), name=str("Gengi"), privilege=const.USER_DEFAULT, password=str(password), group_id='', user_id=str(2))
# zkteco.set_user(uid=int(3), name=str("Antonio"), privilege=const.USER_DEFAULT, password=str(password), group_id='', user_id=str(3))
# zkteco.set_user(uid=int(4), name=str("Fermen"), privilege=const.USER_DEFAULT, password=str(password), group_id='', user_id=str(4))
print str("Done")
cur.execute("INSERT INTO datatable (numerical,id,name,DATE,point,timein,timeout,STATE,timelate) VALUES ("+  str(1) + "," +  str(1) + ",'" + str('Halo') + "'," + `tempstr3` + "," + `1` +"," + `str(hela1)` + "," +`str(hela3)` + "," + `1`+ "," + `str(hela2)` + ")" )
cur.execute("INSERT INTO datatable (numerical,id,name,DATE,point,timein,timeout,STATE,timelate) VALUES ("+  str(2) + "," +  str(2) + ",'" + str('Gengi') + "'," + `tempstr3` + "," + `1` +"," + `str(hela1)` + "," +`str(hela3)` + "," + `1`+ "," + `str(hela2)` + ")" )
cur.execute("INSERT INTO datatable (numerical,id,name,DATE,point,timein,timeout,STATE,timelate) VALUES ("+  str(3) + "," +  str(1) + ",'" + str('Halo') + "'," + `tempstr1` + "," + `100` +"," + `str(hela7)` + "," +`str(hela3)` + "," + `1`+ "," + `str(hela8)` + ")" )
cur.execute("INSERT INTO datatable (numerical,id,name,DATE,point,timein,timeout,STATE,timelate) VALUES ("+  str(4) + "," +  str(2) + ",'" + str('Gengi') + "'," + `tempstr1` + "," + `10` +"," + `str(hela1)` + "," +`str(hela3)` + "," + `1`+ "," + `str(hela2)` + ")" )
cur.execute("INSERT INTO datatable (numerical,id,name,DATE,point,timein,timeout,STATE,timelate) VALUES ("+  str(5) + "," +  str(4) + ",'" + str('Fermen') + "'," + `tempstr4` + "," + `1000000` +"," + `str(hela1)` + "," +`str(hela3)` + "," + `1`+ "," + `str(hela2)` + ")" )

#cur.execute("DELETE from datatable;") 
# for i in range(1, 5):
# 	cur.execute("INSERT INTO datatable (numerical,id,name,DATE,point,timein,timeout,STATE,timelate) VALUES ("+  str(i) + "," +  str(1) + ",'" + str('Henry') + "'," + `tempstr1` + "," + `187` +"," + `str(hela1)` + "," +`str(hela3)` + "," + `1`+ "," + `str(hela2)` + ")" )
# for i in range(5, 10):
# 	cur.execute("INSERT INTO datatable (numerical,id,name,DATE,point,timein,timeout,STATE,timelate) VALUES ("+  str(i) + "," +  str(2) + ",'" + str('Alex') + "'," + `tempstr2` + "," + `121` +"," + `str(hela5)` + "," +`str(hela3)` + "," + `1`+ "," + `str(hela6)` + ")" )
# for i in range(10, 15):
# 	cur.execute("INSERT INTO datatable (numerical,id,name,DATE,point,timein,timeout,STATE,timelate) VALUES ("+  str(i) + "," +  str(3) + ",'" + str('Bobby') + "'," + `tempstr3` + "," + `162` +"," + `str(hela7)` + "," +`str(hela3)` + "," + `1`+ "," + `str(hela8)` + ")" )
# for i in range(16, 20):
# 	cur.execute("INSERT INTO datatable (numerical,id,name,DATE,point,timein,timeout,STATE,timelate) VALUES ("+  str(i) + "," +  str(4) + ",'" + str('Chaly') + "'," + `tempstr4` + "," + `83` +"," + `str(hela9)` + "," +`str(hela3)` + "," + `1`+ "," + `str(hela10)` + ")" )
# # for i in range(1, 80):
# #     zkteco.set_user(uid=i, name='Fanani M. Ihsan', privilege=const.USER_DEFAULT, password='', group_id='', user_id=str(i))

conn.commit()  
