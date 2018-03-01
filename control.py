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
conn = psycopg2.connect(database="postgres", user = "postgres", password = "123", host = "127.0.0.1", port = "6000")
cur = conn.cursor()
print "Database connected"

y = []
y1 = []
z = []
g = []

########## ket noi may cham cong #########
zk = zklib.ZKLib("192.168.1.201", 4370)
statusConnect = zk.connect()
attendance = None
data_user = None
zkteco_users = None
zkteco = None
if statusConnect == True:
    sys.path.append("zk")
    zkteco = ZK('192.168.1.201', port=4370, timeout=2)
    zkteco = zkteco.connect()
    print "connection to device:", statusConnect
    data_user = zk.getUser()
    zkteco_users = zkteco.get_users()
    attendance = zk.getAttendance()
print statusConnect
######### tao ung dung FLASK ###############################################
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required(), validators.Length(min=1, max=20)])
    id = TextField('ID:', validators=[validators.required(), validators.Length(min=1, max=4)])
    password = TextField('Password:', validators=[])


############### tao user #########################################
@app.route("/create", methods=['GET', 'POST'])
def forms():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        form = ReusableForm(request.form)
        print form.errors
        if request.method == 'POST':
            name=request.form['name']
            password=request.form['password']
            id =request.form['id']
            uid =request.form['uid']
            if statusConnect == False:
                flash ('Please connect to fingerprint scanner first !')
            else:
                if id != "" and name != "" and uid != "":
                    temp = 0
                    cur.execute("SELECT * FROM usertable ")
                    usertable = cur.fetchall()
                    for user in usertable:
                        if int(user[1]) == int(id) or int(user[0]) == int(uid): 
                            temp = 1
                    if temp == 0:
                        zkteco.set_user(uid=int(uid), name=str(name), privilege=const.USER_DEFAULT, password=str(password), group_id='', user_id=str(id))
                        flash(' Welcome!  Name: ' + name + " ID:" + id)
                    elif temp == 1:
                        flash ('UID or ID already exist')
                else:  
                    flash('Error:Please type UID, ID, Name ')
        return render_template('create.html', form=form)
######### xoa user ###########################################################
@app.route("/delete", methods=['GET', 'POST'])
def delete():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        form = ReusableForm(request.form)
        print form.errors
        cur.execute("SELECT * FROM usertable")
        usertable = cur.fetchall() 
        if request.method == 'POST':
            name=request.form['name']
            id =request.form['id']
            uid =request.form['uid']
            tempdelete = 0
            if statusConnect == False:
                flash ('Please connect to fingerprint scanner first !')
            else: 
                if id != "" and uid != "" and name != "":
                    for user in usertable:
                        if int(user[0]) == int(uid):
                            tempdelete = 1
                        else: 
                            tempdelete = 2    
                elif id == "" or uid == "" or name == "":
                    flash(' Type ID and UID and name!')  
            if tempdelete == 2:
                flash(' ID and UID does not exist')
            elif tempdelete == 1:
                zkteco.delete_user(uid=int(uid))
                flash ('UID:' + str(user[0]) + '. ID: ' + str(user[1]) + '. Name: ' + str(user[2]))
                flash(' Deleted!')

        return render_template('delete.html', form=form)
 
    
######### show data update ########################################################################
h = []
@app.route("/showdata", methods=['GET', 'POST'])
def showdata():
    flash ('Connect to device:' + str(statusConnect))
    h = []
    cur.execute("SELECT * FROM datatable ")
    rows3 = cur.fetchall()
    for data in rows3:
        if 1000 > data[4] >= 1:
			data = list(data)
			data[4] = 'co mat' 
			data = tuple(data)
        elif 1000000 > data[4] >= 1000:
			data = list(data)
			data[4] = 'nua ngay'
			data = tuple(data)
        elif data[4] >= 1000000:
			data = list(data)
			data[4] = 'ca ngay'
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
    import datetime
    from datetime import datetime, date
    form = ReusableForm(request.form)
    k= []
    print form.errors 
    if request.method == 'POST':
        name=request.form['name']
        id =request.form['id']
        date = request.form['date']
        date1 = request.form['date1']
        cur.execute("SELECT * FROM usertable")
        usertable = cur.fetchall() 
        if str(date) != "" and str(date1) != "":
            flash(str(date)  + " - " + str(date1) )             
            cur.execute("SELECT id, name, SUM(point), SUM(timelate) AS point FROM datatable WHERE date >= '" + str(date) + "' AND date <= '" + str(date1) + "' GROUP BY id, name ")
            dataselect = cur.fetchall()
            d1 = datetime.strptime(date1, "%m/%d/%Y")
            d = datetime.strptime(date, "%m/%d/%Y")
            numberDay = 0
            ## loc thu 7 chu nhat ##############################
            def daterange(start_date, end_date):
                for n in range(int ((end_date - start_date).days)+1):
                    yield start_date + timedelta(n)
            for single_date in daterange(d, d1):
                if 2 <= (single_date.weekday()+2) <= 6:
                    numberDay += 1
                    print single_date.strftime("%Y-%m-%d")
                    print str(single_date.weekday()+2) + "-thu"
            ##### tong so ngay tu From den To ########################
            for user in usertable:
                k.append((user[1],user[2],"None","None",numberDay))
                for data in dataselect:
                    data = list(data)
                    all = str(data[2]/1000000)[:] + " ca ngay - " + str((data[2]%1000000)/1000)[:] + " nua ngay - " + str((data[2]%1000000)%1000)[:] + " quet thieu"
                    nohere = numberDay - (int(data[2])/1000000 + int((data[2])%1000000)/1000 + int((data[2])%1000000)%1000)
                    data = tuple(data) 
                    if user[1] == data[0]:
                        k.remove((user[1],user[2],"None","None",numberDay))
                        k.insert(0,(data[0],data[1],all,data[3],nohere))

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

######### danh sach hoc vien hien tai ############################################
import datetime
from datetime import date, timedelta
@app.route('/useronline/') 
def userOnline():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        y = []
        y1 = []
        currentTime = datetime.datetime.now().strftime ("%Y-%m-%d")
        onedayagoTime = date.today() - timedelta(1)
        twodayagoTime = date.today() - timedelta(2)
        threedayagoTime = date.today() - timedelta(3)
        cur.execute("SELECT * FROM usertable")
        usertable = cur.fetchall() 
        cur.execute("SELECT * FROM datatable")
        datatable = cur.fetchall() 
        cur.execute("SELECT * FROM datatable WHERE date = " + `str(currentTime)` )
        datatemp = cur.fetchall() 

        for data in datatemp:  
            if 1000 > data[4] >= 1:
                data = list(data)
                data[4] = 'co mat' 
                data = tuple(data)
            elif 1000000 > data[4] >= 1000:
                data = list(data)
                data[4] = 'nua ngay'
                data = tuple(data)
            elif data[4] >= 1000000:
                data = list(data)
                data[4] = 'ca ngay'
                data = tuple(data) 
            y.insert(0,(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]))
        #### thong ke 3 ngay gan day #######################################
        for user in usertable:
            threedayago = cur.execute("SELECT point FROM datatable WHERE (date,id)  = " + " ( "+ `str(threedayagoTime)` +"," + str(user[1]) + ")" )        
            threedayago = cur.fetchall()
            twodayago = cur.execute("SELECT point FROM datatable WHERE (date,id)  = " + " ( "+ `str(twodayagoTime)` +"," + str(user[1]) + ")" )        
            twodayago = cur.fetchall()
            onedayago = cur.execute("SELECT point FROM datatable WHERE (date,id)  = " + " ( "+ `str(onedayagoTime)` +"," + str(user[1]) + ")" )        
            onedayago = cur.fetchall()
            today = cur.execute("SELECT point FROM datatable WHERE (date,id)  = " + " ( "+ `str(currentTime)` +"," + str(user[1]) + ")" )     
            today = cur.fetchall()
            for data in twodayago:
                twodayago = data[0]
            for data in onedayago:
                onedayago = data[0]
            for data in threedayago:
                threedayago = data[0]
            for data in today:
                today = data[0]
            #
            if threedayago == 1000000:
                threedayago = "ca ngay"
            elif threedayago == 1000:
                threedayago = "nua ngay"
            elif not threedayago:
                threedayago = "nghi"
            #
            if twodayago == 1000000:
                twodayago = "ca ngay"
            elif twodayago == 1000:
                twodayago = "nua ngay"
            elif not twodayago:
                twodayago = "nghi"
            #
            if onedayago == 1000000:
                onedayago = "ca ngay"
            elif onedayago == 1000:
                onedayago = "nua ngay"
            elif not onedayago:
                onedayago = "nghi"
                #
            if not today:
                today = "nghi"
            y1.insert(0,(user[1],user[2],threedayago,twodayago,onedayago,today)) 

            for data in datatemp:
                if data[1] == user[1]:
                    y1.remove((user[1],user[2],threedayago,twodayago,onedayago,today))        
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