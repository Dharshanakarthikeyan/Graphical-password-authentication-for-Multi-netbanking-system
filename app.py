# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session

from flask_mysqldb import MySQL
from datetime import date
import MySQLdb.cursors

from twilio.rest import Client
import re
import os
import config

from PIL import Image
import PIL
app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'

app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = ''

app.config['MYSQL_DB'] = 'bank_multi'

mysql = MySQL(app)


UPLOAD_FOLDER = 'static'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('index.html')
@app.route('/coordinate', methods=['GET', 'POST'])
def coordinate():
    msg = ''
    print("register2")
    if request.method == 'POST' and 'x' in request.form and 'y' in request.form and 'uname' in request.form:

        x = request.form['x']

        y = request.form['y']

        uname = request.form['uname']
        print(x)
        print(y)
        print(uname)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE user_reg set xvalue = %s, yvalue = %s WHERE uname = %s', (x, y, uname))

        sql = "UPDATE user_reg set xvalue = %s, yvalue = %s WHERE uname = %s"

        val = (x, y, uname)
        cursor.execute(sql, val)

        mysql.connection.commit()

        msg = 'You have successfully registered !'
        return render_template('index.html')

    return render_template('index.html')


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST' and 'uname' in request.form:
        uname = request.form['uname']
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], uname + "." + file1.filename)
        fname = uname + "." + file1.filename


        print(file1)
        file1.save(path)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE user_reg set image = %s WHERE uname = % s', (fname, uname))

        sql = "UPDATE user_reg SET image = %s WHERE uname = %s"

        val = (fname, uname)
        cursor.execute(sql, val)

        mysql.connection.commit()

        msg = 'You have successfully registered !'
        return render_template('register2.html', uname=uname, fname=fname)
    else:

        uname = request.form['uname']
        msg = 'Incorrect username / password !'

    return render_template('register2.html', msg=msg, uname=uname)


@app.route('/mgrlogin', methods=['GET', 'POST'])
def mgrlogin():
    msg = ''
    print("mgrlogin")
    if request.method == 'POST' and 'uname' in request.form and 'pword' in request.form:

        uname = request.form['uname']

        pword = request.form['pword']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM manager WHERE uname = % s AND pass = % s', (uname, pword))

        account = cursor.fetchone()

        if account:

            session['loggedin'] = True

            session['id'] = account['id']

            session['username'] = account['uname']
            session['bank'] = account['bank']
            session['branch'] = account['branch']

            bank = account['bank']
            branch = account['branch']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor = mysql.connection.cursor()
            cur = cursor.execute("SELECT * FROM user_acct WHERE bank= % s AND branch = % s", (bank, branch))
            colour = cursor.fetchall()

            print(colour)
            return render_template('mgrhome.html', uname=uname, bank=bank, branch=branch, colour=colour)
        else:

            msg = 'Incorrect username / password !'

    return render_template('index_mgr.html', msg=msg)


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    msg = ''

    if request.method == 'POST' and 'uname' in request.form and 'pword' in request.form:

        uname = request.form['uname']

        pword = request.form['pword']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM admin_login WHERE uname = % s AND passw = % s', (uname, pword))

        account = cursor.fetchone()

        if account:

            session['loggedin'] = True

            session['id'] = account['id']

            session['username'] = account['uname']


            cursor = mysql.connection.cursor()
            cur = cursor.execute("SELECT bank FROM bank")
            colour = cursor.fetchall()
            res = [i[0] for i in colour]
            print(res)
            rows = [*set(res)]
            print(rows)

            cur1 = cursor.execute("SELECT branch FROM bank")
            colour1 = cursor.fetchall()
            res1 = [i1[0] for i1 in colour1]
            print(res1)
            rows1 = [*set(res1)]
            print(rows1)

            return render_template('add.html', rows=rows, rows1=rows1)
        else:

            msg = 'Incorrect username / password !'

    return render_template('index_admin.html', msg=msg)

@app.route('/mcheckcoordinate', methods=['GET', 'POST'])
def mcheckcoordinate():
    msg = ''
    print("checked")
    if request.method == 'POST' and 'uname' in request.form and 'x' in request.form and 'y' in request.form:

        uname = request.form['uname']

        x = request.form['x']
        y = request.form['y']

        print(x)

        print(y)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM manager WHERE uname = %s AND xvalue = % s AND yvalue = % s', (uname, x, y))

        account = cursor.fetchone()
        fname = account['image']
        xvalue=account['xvalue']

        print(xvalue)
        yvalue = account['yvalue']
        if account:

            session['loggedin'] = True

            session['id'] = account['id']

            session['username'] = account['uname']

            msg = 'Logged In Successfully !'
            return render_template('mgrhome.html', uname=uname, fname=fname, xvalue=xvalue, yvalue=yvalue)

        else:

            msg = 'Incorrect username / password !'

    return render_template('index_mgr.html', msg=msg)


@app.route('/checkcoordinate', methods=['GET', 'POST'])
def checkcoordinate():
    msg = ''
    print("checked")
    if request.method == 'POST' and 'uname' in request.form and 'x' in request.form and 'y' in request.form:

        uname = request.form['uname']

        x = request.form['x']
        y = request.form['y']

        print(x)

        print(y)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM user_reg WHERE uname = %s AND xvalue = % s AND yvalue = % s', (uname, x, y))

        account = cursor.fetchone()
        if account:

            fname = account['image']
            xvalue = account['xvalue']

            print(xvalue)
            yvalue = account['yvalue']
            session['loggedin'] = True

            session['id'] = account['id']

            session['username'] = account['uname']

            msg = 'Logged In Successfully !'
            return render_template('userhome.html', uname=uname, fname=fname, xvalue=xvalue, yvalue=yvalue)

        else:

            msg = 'Wrong Coordinates!'

            return render_template('login.html', msg=msg)

    return render_template('login.html', msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''



    if request.method == 'POST' and 'uname' in request.form and 'pword' in request.form:

        uname = request.form['uname']

        pword = request.form['pword']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM user_reg WHERE uname = % s AND passw = % s', (uname, pword))

        account = cursor.fetchone()
        if account:

            fname = account['image']
            xvalue = account['xvalue']
            yvalue = account['yvalue']
            session['loggedin'] = True

            session['id'] = account['id']

            session['username'] = account['uname']

            msg = 'Logged In Successfully !'
            # sendsms
            account_sid = config.TWILIO_ACCOUNT_SID
            auth_token = config.TWILIO_AUTH_TOKEN

            client = Client(account_sid, auth_token)

            def send_sms():
                # global client
                message = client.messages.create(
                    body='Your Account is loggedIn',
                    from_='+18329796131',
                    to='+918870965055'
                )
                return message.sid

            print(send_sms())



            return render_template('login1.html', uname=uname, fname=fname, xvalue=xvalue, yvalue=yvalue)

        else:

            msg = 'Incorrect username / password !'

            return render_template('login.html', msg=msg)

    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)

    session.pop('id', None)

    session.pop('username', None)

    return render_template('index.html')


@app.route('/createaccountcode', methods=['GET', 'POST'])
def createaccountcode():
    msg = ''
    print("createaccountcode")
    if request.method == 'POST' and 'bank' in request.form and 'ifsc' in request.form and 'branch' in request.form and 'accountenter' in request.form:

        uname = session['username']


        bank = request.form['bank']

        branch = request.form['branch']


        ifsc = request.form['ifsc']

        accountenter = request.form['accountenter']
        print(bank)
        print(branch)
        print(ifsc)
        print(accountenter)

        used = "1"
        used0 = "0"

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_acct ORDER BY id DESC LIMIT 0, 1')
        account = cursor.fetchone()
        newid = account['id'] + 1
        print(newid)

        cursor.execute('SELECT * FROM account WHERE account = % s AND bank = % s AND used = % s',
                       (accountenter, bank, '0',))
        account1 = cursor.fetchone()

        sql = "INSERT INTO user_acct (id,uname,bank,branch,account) VALUES (%s, %s, %s, %s, %s)"

        val = (newid, uname, bank, branch, accountenter)
        cursor.execute(sql, val)
        print("insert success")

        mysql.connection.commit()
        cursor.execute(
            'UPDATE account SET used = % s WHERE account = % s',
            (used, accountenter,))

        mysql.connection.commit()
        print("update success")

        msg = 'You have successfully registered !'
        return render_template('account.html', uname=uname, msg=msg)



    elif request.method == 'POST':

        msg = 'Please fill out the form !'

    return render_template('account.html', msg=msg)


@app.route('/addmanager', methods=['GET', 'POST'])
def addmanager():
    msg = ''
    print("add manager")
    if request.method == 'POST' and 'mname' in request.form and 'contact' in request.form and 'email' in request.form and 'bank' in request.form and 'branch' in request.form:

        mname = request.form['mname']

        contact = request.form['contact']

        email = request.form['email']

        bank = request.form['bank']

        branch = request.form['branch']


        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM manager ORDER BY id DESC LIMIT 0, 1')
        account = cursor.fetchone()
        newid= account['id'] + 1
        code ="M"
        pwd = "PWD"
        uname = str(code) + str(newid)
        passw = str(code) + str(newid) + str(pwd)
        print(uname)
        print(passw)
        today = str(date.today())
        print(today)


        sql = "INSERT INTO manager (id,name,contact,email,bank,branch,uname,pass,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        val = (newid, mname, contact, email, bank, branch, uname, passw, today)
        cursor.execute(sql, val)

        mysql.connection.commit()


        # sendsms
        account_sid = config.TWILIO_ACCOUNT_SID
        auth_token = config.TWILIO_AUTH_TOKEN

        client = Client(account_sid, auth_token)

        def send_sms():
            # global client
            message = client.messages.create(
                body='username' + " " + uname + " " + 'Password' + " " + passw,
                from_='+18329796131',
                to='+918870965055'
            )
            return message.sid

        print(send_sms())
        msg = 'Added Manager successfully!'
        cursor = mysql.connection.cursor()
        cur = cursor.execute("SELECT bank FROM bank")
        colour = cursor.fetchall()
        res = [i[0] for i in colour]
        print(res)
        rows = [*set(res)]
        print(rows)

        cur1 = cursor.execute("SELECT branch FROM bank")
        colour1 = cursor.fetchall()
        res1 = [i1[0] for i1 in colour1]
        print(res1)
        rows1 = [*set(res1)]
        print(rows1)

        return render_template('add.html', uname=uname, msg=msg, rows=rows, rows1=rows1)


    elif request.method == 'POST':

        msg = 'Please fill out the form !'
    cursor = mysql.connection.cursor()
    cur = cursor.execute("SELECT bank FROM bank")
    colour = cursor.fetchall()
    res = [i[0] for i in colour]
    print(res)
    rows = [*set(res)]
    print(rows)

    cur1 = cursor.execute("SELECT branch FROM bank")
    colour1 = cursor.fetchall()
    res1 = [i1[0] for i1 in colour1]
    print(res1)
    rows1 = [*set(res1)]
    print(rows1)

    uname = session['username']
    return render_template('add.html', uname=uname, msg=msg, rows=rows, rows1=rows1)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    print("register")
    if request.method == 'POST' and 'name' in request.form and 'gender' in request.form and 'dob' in request.form and 'address1' in request.form and 'contact' in request.form and 'email1' in request.form and 'uname' in request.form and 'passw' in request.form and 'cpass' in request.form and 'skey' in request.form:

        name = request.form['name']

        gender = request.form['gender']

        dob = request.form['dob']

        address1 = request.form['address1']

        contact = request.form['contact']

        email1 = request.form['email1']

        uname = request.form['uname']

        passw = request.form['passw']

        cpass = request.form['cpass']

        skey = request.form['skey']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM user_reg WHERE uname = % s', (uname,))

        account = cursor.fetchone()

        if account:

            msg = 'Account already exists !'

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email1):

            msg = 'Invalid email address !'

        elif not re.match(r'[A-Za-z0-9]+', uname):

            msg = 'name must contain only characters and numbers !'

        else:

            sql = "INSERT INTO user_reg (name, gender, dob, address, contact, email, uname, passw, secret) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            val = (name, gender, dob, address1, contact, email1, uname, passw, skey)
            cursor.execute(sql, val)

            mysql.connection.commit()

            msg = 'You have successfully registered !'
            return render_template('register1.html', uname=uname)

    elif request.method == 'POST':

        msg = 'Please fill out the form correctly !'

        return render_template('register.html', msg=msg)

    return render_template('register.html', msg=msg)

@app.route("/admin")
def admin():
    return render_template("index_admin.html")

@app.route("/manager")
def manager():
    return render_template("index_mgr.html")



@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")

    return redirect(url_for('login'))


@app.route("/display")
def display():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'],))

        account = cursor.fetchone()

        return render_template("display.html", account=account)

    return redirect(url_for('login'))

@app.route("/mchangepwd", methods=['GET', 'POST'])
def mchangepwd():
    msg = ''

    if 'loggedin' in session:

        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:

            username = request.form['username']

            password = request.form['password']

            email = request.form['email']

            organisation = request.form['organisation']

            address = request.form['address']

            city = request.form['city']

            state = request.form['state']

            country = request.form['country']

            postalcode = request.form['postalcode']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute('SELECT * FROM accounts WHERE username = % s', (username,))

            account = cursor.fetchone()

            if account:

                msg = 'Account already exists !'

            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):

                msg = 'Invalid email address !'

            elif not re.match(r'[A-Za-z0-9]+', username):

                msg = 'name must contain only characters and numbers !'

            else:

                cursor.execute(
                    'UPDATE accounts SET  username =% s, password =% s, email =% s, organisation =% s, address =% s, city =% s, state =% s, country =% s, postalcode =% s WHERE id =% s',
                    (username, password, email, organisation, address, city, state, country, postalcode,
                     (session['id'],),))

                mysql.connection.commit()

                msg = 'You have successfully updated !'

        elif request.method == 'POST':

            msg = 'Please fill out the form !'

        return render_template("update.html", msg=msg)

    return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''

    if 'loggedin' in session:

        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:

            username = request.form['username']

            password = request.form['password']

            email = request.form['email']

            organisation = request.form['organisation']

            address = request.form['address']

            city = request.form['city']

            state = request.form['state']

            country = request.form['country']

            postalcode = request.form['postalcode']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute('SELECT * FROM accounts WHERE username = % s', (username,))

            account = cursor.fetchone()

            if account:

                msg = 'Account already exists !'

            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):

                msg = 'Invalid email address !'

            elif not re.match(r'[A-Za-z0-9]+', username):

                msg = 'name must contain only characters and numbers !'

            else:

                cursor.execute(
                    'UPDATE accounts SET  username =% s, password =% s, email =% s, organisation =% s, address =% s, city =% s, state =% s, country =% s, postalcode =% s WHERE id =% s',
                    (username, password, email, organisation, address, city, state, country, postalcode,
                     (session['id'],),))

                mysql.connection.commit()

                msg = 'You have successfully updated !'

        elif request.method == 'POST':

            msg = 'Please fill out the form !'

        return render_template("update.html", msg=msg)

    return redirect(url_for('login'))

@app.route("/adminhome")
def adminhome():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor = mysql.connection.cursor()
    cur = cursor.execute("SELECT * FROM bank")
    colour = cursor.fetchall()

    print(colour)
    return render_template("adminhome.html", colour=colour)

@app.route("/add")
def add():
    cursor = mysql.connection.cursor()
    cur = cursor.execute("SELECT bank FROM bank")
    colour = cursor.fetchall()
    res = [i[0] for i in colour]
    print(res)
    rows = [*set(res)]
    print(rows)

    cur1 = cursor.execute("SELECT branch FROM bank")
    colour1 = cursor.fetchall()
    res1 = [i1[0] for i1 in colour1]
    print(res1)
    rows1 = [*set(res1)]
    print(rows1)

    return render_template('add.html', rows=rows, rows1=rows1)

@app.route("/mgrhome")
def mgrhome():

    return render_template("mgrhome.html")


@app.route('/b1')
def b1():
    if 'username' in session:
        uname = session['username']

        session['loggedin'] = True
        bank1 = request.args.get('bank', None)
        session['bank'] = bank1
        bank = session['bank']

        return render_template("userhome1.html",bank=bank,uname=uname)
@app.route('/b2')
def b2():
    if 'username' in session:
        uname = session['username']
        session['loggedin'] = True
        bank1 = request.args.get('bank', None)
        session['bank'] = bank1
        bank = session['bank']

        return render_template("userhome1.html",bank=bank,uname=uname)
@app.route('/b3')
def b3():
    if 'username' in session:
        uname = session['username']
        session['loggedin'] = True
        bank1 = request.args.get('bank', None)
        session['bank'] = bank1
        bank = session['bank']

        return render_template("userhome1.html",bank=bank,uname=uname)

@app.route('/b4')
def b4():
    if 'username' in session:
        uname = session['username']
        session['loggedin'] = True
        bank1 = request.args.get('bank', None)
        session['bank'] = bank1
        bank = session['bank']

        return render_template("userhome1.html",bank=bank,uname=uname)

@app.route('/b5')
def b5():
    if 'username' in session:
        uname = session['username']
        session['loggedin'] = True
        bank1 = request.args.get('bank', None)
        session['bank'] = bank1
        bank = session['bank']

        return render_template("userhome1.html",bank=bank,uname=uname)

@app.route('/b6')
def b6():
    if 'username' in session:
        uname = session['username']
        session['loggedin'] = True
        bank1 = request.args.get('bank', None)
        session['bank'] = bank1
        bank = session['bank']

        return render_template("userhome1.html",bank=bank,uname=uname)

@app.route('/b7')
def b7():
    if 'username' in session:
        uname = session['username']
        session['loggedin'] = True
        bank1 = request.args.get('bank', None)
        session['bank'] = bank1
        bank = session['bank']

        return render_template("userhome1.html",bank=bank,uname=uname)

@app.route('/b8')
def b8():
    if 'username' in session:
        uname = session['username']
        session['loggedin'] = True
        bank1 = request.args.get('bank', None)
        session['bank'] = bank1
        bank = session['bank']

        return render_template("userhome1.html",bank=bank,uname=uname)

@app.route('/b9')
def b9():
    if 'username' in session:
        uname = session['username']
        session['loggedin'] = True
        bank1 = request.args.get('bank', None)
        session['bank'] = bank1
        bank = session['bank']

        return render_template("userhome1.html",bank=bank,uname=uname)


@app.route('/b10')
def b10():
    if 'username' in session:
        uname = session['username']
        session['loggedin'] = True
        bank1 = request.args.get('bank', None)
        session['bank'] = bank1
        bank = session['bank']

        return render_template("userhome1.html",bank=bank,uname=uname)

@app.route('/b11')
def b11():
    if 'username' in session:
        uname = session['username']
        session['loggedin'] = True
        bank1 = request.args.get('bank', None)
        session['bank'] = bank1
        bank = session['bank']

        return render_template("userhome1.html",bank=bank,uname=uname)


@app.route('/b12')
def b12():
    if 'username' in session:
        uname = session['username']
        session['loggedin'] = True
        bank1 = request.args.get('bank', None)
        session['bank'] = bank1
        bank = session['bank']

        return render_template("userhome1.html",bank=bank,uname=uname)


@app.route('/b13')
def b13():
    if 'username' in session:
        uname = session['username']
        session['loggedin'] = True
        bank1 = request.args.get('bank', None)
        session['bank'] = bank1
        bank = session['bank']

        return render_template("userhome1.html",bank=bank,uname=uname)

@app.route('/b14')
def b14():
    if 'username' in session:
        uname = session['username']
        session['loggedin'] = True
        bank1 = request.args.get('bank', None)
        session['bank'] = bank1
        bank = session['bank']
        return render_template("userhome1.html",bank=bank,uname=uname)

@app.route('/userhome0')
def userhome0():
    if 'username' in session:
        uname = session['username']

        return render_template("userhome.html",uname=uname)

@app.route('/accountdetails')
def accountdetails():
    if 'username' in session:
        uname = session['username']

        bank = session['bank']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user_acct WHERE uname = % s AND bank = % s", (uname, bank,))
        rows = cursor.fetchone()
        bank = rows[2]
        branch = rows[3]
        acc = rows[4]
        session['acc'] = acc
        session['bank'] = bank
        session['branch'] = branch
        cursor.execute('SELECT * FROM bank WHERE bank = % s AND branch = % s', (bank, branch))
        colour1 = cursor.fetchone()
        ifsc = colour1[3]
        session['ifsc'] = ifsc
        return render_template("account_det.html",uname=uname,bank=bank,branch=branch,acc=acc,ifsc=ifsc)


@app.route('/checkbalance', methods=['GET', 'POST'])
def checkbalance():


    if request.method == 'POST' and 'acc' in request.form and 'bank' in request.form:
        uname = session['username']
        bank = request.form['bank']


        acc = request.form['acc']
        print(acc)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user_acct WHERE uname = % s AND bank = % s AND account = % s", (uname, bank, acc,))
        rows = cursor.fetchone()
        print(rows)
        balance = rows[5]

        return render_template("balance.html",uname=uname,bank=bank,acc=acc,balance=balance)

@app.route('/createaccount')
def createaccount():
    if 'username' in session:
        uname = session['username']

        bank = session['bank']
        print(bank)
        cursor = mysql.connection.cursor()
        cur = cursor.execute("SELECT bank FROM bank")
        colour = cursor.fetchall()
        res = [i[0] for i in colour]
        print(res)
        rows = [*set(res)]
        print(rows)

        cur1 = cursor.execute("SELECT ifsc FROM bank")
        colour1 = cursor.fetchall()
        res1 = [i1[0] for i1 in colour1]
        print(res1)
        rows1 = [*set(res1)]
        print(rows1)

        cur2 = cursor.execute("SELECT branch FROM bank")
        colour2 = cursor.fetchall()
        res2 = [i2[0] for i2 in colour2]
        print(res2)
        rows2 = [*set(res2)]
        print(rows2)
        return render_template("account.html",uname=uname,bank=bank,rows=rows,rows1=rows1,rows2=rows2)

@app.route('/balance')
def balance():
    if 'username' in session:
        uname = session['username']
        bank = session['bank']
        acc = session['acc']
        return render_template("balance.html",uname=uname,bank=bank,acc=acc)

@app.route('/transfer')
def transfer():
    if 'username' in session:
        uname = session['username']
        bank = session['bank']
        acc = session['acc']
        ifsc = session['ifsc']
        branch = session['branch']

        cursor = mysql.connection.cursor()
        cur = cursor.execute("SELECT bank FROM bank")
        colour = cursor.fetchall()
        res = [i[0] for i in colour]
        print(res)
        rows = [*set(res)]
        print(rows)

        return render_template("transfer.html",uname=uname,bank=bank,acc=acc,ifsc=ifsc,branch=branch,rows=rows)

@app.route('/mactivate', methods=['GET', 'POST'])
def mactivate():
    msg = ''
    print("mactivate")
    if request.method == 'POST' and 'account' in request.form:

        uname = session['username']

        bank = session['bank']
        branch = session['branch']
        account = request.form['account']
        print(account)
        amount = "5000"
        status = "1"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            'UPDATE user_acct SET deposit = % s, status = % s WHERE account = % s ',
            (amount, status, account, ))

        mysql.connection.commit()
        print("update1 success")

        msg = 'Account Activated'

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cur = cursor.execute("SELECT * FROM user_acct WHERE bank= % s AND branch = % s", (bank, branch))
        colour = cursor.fetchall()

        print(colour)
        return render_template('mgrhome.html', uname=uname, bank=bank, branch=branch, colour=colour,msg=msg)


    elif request.method == 'POST':

        msg = 'Please fill out the form !'
    uname = session['username']
    return render_template("mgrhome.html", uname=uname, msg=msg)


@app.route('/transferamt', methods=['GET', 'POST'])
def transferamt():
    msg = ''
    print("transferamt")
    if request.method == 'POST' and 'mybank' in request.form and 'myifsc' in request.form and 'mybranch' in request.form and 'myacc' in request.form and 'toacc' in request.form and 'tobank' in request.form and 'amount' in request.form and 'skey' in request.form:

        uname = session['username']


        mybank = request.form['mybank']
        branch = request.form['mybranch']
        ifsc = request.form['myifsc']
        myacc = request.form['myacc']
        toacc = request.form['toacc']
        tobank = request.form['tobank']

        amount = request.form['amount']
        skey = request.form['skey']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user_acct WHERE account = % s AND bank = % s",
                       (myacc, mybank,))
        rows = cursor.fetchone()
        print(rows)
        depositold = rows['deposit']

        print(depositold)
        depositnew = int(depositold) - int(amount)
        print(depositnew)
        cursor.execute(
            'UPDATE user_acct SET deposit = % s WHERE account = % s',
            (depositnew, myacc,))

        mysql.connection.commit()
        print("update1 success")

        cursor.execute("SELECT * FROM user_acct WHERE account = % s AND bank = % s",
                       (toacc, tobank,))


        rows2 = cursor.fetchone()
        print(rows2)
        depositold1 = rows2['deposit']
        depositnew1 = int(depositold1) + int(amount)
        print(depositold1)
        print(depositnew1)
        cursor.execute(
            'UPDATE user_acct SET deposit = % s WHERE account = % s',
            (depositnew1, toacc,))

        mysql.connection.commit()
        print("update2 success")
        today = date.today()

        sql = "INSERT INTO transfer (uname,bank,account,bank2,account2,amount,rdate) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        val = (uname, mybank, myacc, tobank, toacc, amount, today)
        cursor.execute(sql, val)
        print("insert success")

        mysql.connection.commit()


        cursor = mysql.connection.cursor()
        cur = cursor.execute("SELECT bank FROM bank")
        colour = cursor.fetchall()
        res = [i[0] for i in colour]
        print(res)
        rows = [*set(res)]
        print(rows)
        msg = 'Amount transferred'
        return render_template("transfer.html",msg=msg,uname=uname,bank=mybank,acc=myacc,ifsc=ifsc,branch=branch,rows=rows)


    elif request.method == 'POST':

        msg = 'Please fill out the form !'
        uname = session['username']
        bank = session['bank']
        acc = session['acc']
        ifsc = session['ifsc']
        branch = session['branch']
        cursor = mysql.connection.cursor()
        cur = cursor.execute("SELECT bank FROM bank")
        colour = cursor.fetchall()
        res = [i[0] for i in colour]
        print(res)
        rows = [*set(res)]
        print(rows)
    return render_template("transfer.html", uname=uname, bank=bank, acc=acc, ifsc=ifsc, branch=branch, rows=rows)


@app.route("/a_view_mgr")
def a_view_mgr():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor = mysql.connection.cursor()
    cur = cursor.execute("SELECT * FROM manager")
    colour = cursor.fetchall()

    print(colour)
    return render_template("a_view_mgr.html", colour=colour)



if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))