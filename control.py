import sys
import json
sys.path.append("zklib")
from zklib import zklib
from zk import ZK, const
import datetime
import time
import zkconst
from time import sleep
from flask import Flask, flash, redirect, render_template, request, session, abort
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os
from datetime import datetime, date, time
import psycopg2
from time import gmtime, strftime

########## ket noi database #########
conn = psycopg2.connect(database="postgres", user = "postgres", password = "123", host = "127.0.0.1", port = "5432")
cur = conn.cursor()
print "Database connected"

y = []
y1 = []
z = []
g = []

########## ket noi may cham cong #########
# zk = zklib.ZKLib("192.168.1.201", 4370)
# ret = zk.connect()
# sys.path.append("zk")
# zkteco = None
# zkteco = ZK('192.168.1.201', port=4370, timeout=5)
# zkteco = zkteco.connect()
# print "connection to device:", ret
# data_user = zk.getUser()
# zkteco_users = zkteco.get_users()
# attendance = zk.getAttendance()

######### tao ung dung FLASK ###############################################
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required(), validators.Length(min=1, max=20)])
    id = TextField('ID:', validators=[validators.required(), validators.Length(min=1, max=4)])
    password = TextField('Password:', validators=[])


############### tao user #########################################
# @app.route("/create", methods=['GET', 'POST'])
# def forms():
#     if not session.get('logged_in'):
#         return render_template('login.html')
#     else:
#         form = ReusableForm(request.form)
#         print form.errors
#         if request.method == 'POST':
#             name=request.form['name']
#             password=request.form['password']
#             id =request.form['id']
#             uid =request.form['uid']
#             if id != "" and name != "" and uid != "":
#                 temp = 0
#                 for user in zkteco_users:
#                     if int(user.uid) == int(id) or int(user.user_id) == int(uid): 
#                         temp = 1
#                 sleep (1)
#                 if temp == 0:
#                     flash(' Welcome!  Name: ' + name + " ID:" + id)
#                     zkteco.set_user(uid=int(uid), name=str(name), privilege=const.USER_DEFAULT, password=str(password), group_id='', user_id=str(id))
#                 elif temp == 1:
#                     flash ('UID or ID already exist')
#             else:  
#                 flash('Error:Please type UID, ID, Name ')
#         return render_template('create.html', form=form)
######### xoa user ###########################################################
# @app.route("/delete", methods=['GET', 'POST'])
# def delete():
#     if not session.get('logged_in'):
#         return render_template('login.html')
#     else:
#         form = ReusableForm(request.form)
#         print form.errors
#         if request.method == 'POST':
#             name=request.form['name']
#             id =request.form['id']
#             id1 =request.form['id1']
#             uid =request.form['uid'] 
#             if id != "":
#                 for user in zkteco_users:
#                     if int(user.user_id) == int(id): 
#                         flash ('UID:' + str(user.uid) + '. ID: ' + str(user.user_id) + '. Name: ' + str(user.name))
#             if id1 != "" and uid != "" and name != "":
#                 flash(' Deleted!')
#                 zkteco.delete_user(uid=int(uid))     
#         return render_template('delete.html', form=form)
 
    
######### show data update ########################################################################
h = []
@app.route("/showdata", methods=['GET', 'POST'])
def showdata():
    flash ('Connect to device:' + str(123))
    h = []
    cur.execute("SELECT * FROM datatable ")
    rows3 = cur.fetchall()
    for data in rows3:
        if 10 > data[4] >= 1:
			data = list(data)
			data[4] = 'at' 
			data = tuple(data)
        elif 100 > data[4] >= 10:
			data = list(data)
			data[4] = 'half day'
			data = tuple(data)
        elif data[4] >= 100:
			data = list(data)
			data[4] = 'full day'
			data = tuple(data)
        data = list(data)
        data = tuple(data) 
        h.insert(0,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]))
    return render_template('showdata.html', showdata = h)
    
########## lay input de hien thi thong ke ##########################################################
@app.route("/get", methods=['GET', 'POST'])
def get():
    form = ReusableForm(request.form)
    print form.errors
    return render_template('get.html', form=form)
       
########## hien thi thong ke #######################################################################
k= []
@app.route("/statistic", methods=['GET', 'POST'])
def statistic():
    k= []
    form = ReusableForm(request.form)
    print form.errors 
    if request.method == 'POST':
        name=request.form['name']
        id =request.form['id']
        date = request.form['date']
        date1 = request.form['date1']
        if str(date) != "" and str(date1) != "":    
            flash(str(date)  + " - " + str(date1) ) 
            cur.execute("SELECT id, name, SUM(point), SUM(timelate) AS point FROM datatable WHERE date >= '" + str(date) + "' AND date <= '" + str(date1) + "' GROUP BY id, name ")
            rows3 = cur.fetchall()
            for data in rows3:
                data = list(data)
                data[2] = str(data[2]/100)[:] + " ngay - " + str((data[2]%100)/10)[:] + " sang/chieu - " + str((data[2]%100)%10)[:] + " quet thieu"
                data = tuple(data) 
                k.insert(0,(data[0],data[1],data[2],data[3]))
    return render_template('statistic.html', statistic = k)
######### list user ############################################
@app.route('/user/') 
def user():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        y = []
        cur.execute("SELECT * FROM usertable")
        rows3 = cur.fetchall() 
        for data in rows3:
            y.insert(0,(data[0],data[1],data[2],data[3]))
        return render_template('user.html', user=y)

######### list user ############################################
import datetime
from datetime import date, timedelta
@app.route('/useronline/') 
def userOnline():
    # ifs not session.get('logged_in'):
    #     return render_template('login.html')
    # else:
    y = []
    y1 = []
    currentTime = datetime.datetime.now().strftime ("%Y-%m-%d")
    yesterday = date.today() - timedelta(1)
    cur.execute("SELECT * FROM usertable")
    usertable = cur.fetchall() 
    cur.execute("SELECT * FROM datatable")
    datatable = cur.fetchall() 
    cur.execute("SELECT * FROM datatable WHERE date = " + `str(currentTime)` )
    datatemp = cur.fetchall() 
    print currentTime  
    print yesterday
    theDayBeforeYesterday = 0
    today = 0
    for data in datatemp:
        y.insert(0,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]))
    for user in usertable:
        y1.insert(0,(user[1],user[2],theDayBeforeYesterday,yesterday,today)) 
        for data in datatemp:
            if data[1] == user[1]:
                y1.remove((user[1],user[2],theDayBeforeYesterday,yesterday,today))        
    print y1
    return render_template('userOnline.html', userOnline = y, userOffnline = y1 )
 
######### auth ############################################
@app.route('/auth')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('admin.html')
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return showdata()

@app.route("/")
def none():
    session['logged_in'] = False
    return showdata()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=8080)