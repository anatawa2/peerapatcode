from flask import Flask, request, session, render_template, redirect, url_for, jsonify, flash
from flask.sessions import NullSession
from werkzeug.utils import secure_filename
import pymysql.cursors
import requests  # LINE
import re
import os

app = Flask(__name__)
conn = pymysql.connect(host='localhost', user='root', password='', db='rmuti',)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def ownpath(seat_id, user_id):
    location = ''
    location = seat_id + '/' + user_id + '/'
    return location


app.secret_key = 'superman'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

maindir = 'static/uploads/'
subdir = ''


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def InsertBlob():
    last_upload = ''
    cur = conn.cursor()
    cur.execute('SELECT * FROM pics WHERE seat_id = %s AND user_id = %s ',
                ([session['seat']], [session['id']]))
    acc = cur.fetchone()
    if acc:
        last_upload = acc[1]

    global subdir
    subdir = ownpath(session['seat'], str(session['id']))

    FilePath = request.files['file']
    if FilePath and allowed_file(FilePath.filename):
        filename = secure_filename(FilePath.filename)

        if last_upload:
            os.remove(maindir + subdir + last_upload.decode())
            cur = conn.cursor()
            cur.execute("UPDATE pics SET img = Null WHERE seat_id = %s AND user_id = %s",
                        (session['seat'], session['id']))
            conn.commit()

        path = os.path.join(maindir, subdir)
        if not os.path.exists(path):
            os.makedirs(path)
        FilePath.save(os.path.join(maindir + subdir, filename))
        if not acc:
            cur.execute('INSERT INTO pics(img, seat_id, user_id) VALUES (%s, %s, %s) ',
                        (filename, [session['seat']], [session['id']]))
            conn.commit()
        else:
            cur.execute("UPDATE pics SET img = %s WHERE seat_id = %s AND user_id = %s",
                        (filename, [session['seat']], [session['id']]))
            conn.commit()

        return redirect(url_for('profile'))


@app.route("/upload2", methods=["POST"])
def InsertBlob2():
    last_upload = ''
    cur = conn.cursor()
    cur.execute('SELECT * FROM pics WHERE seat_id = %s AND user_id = %s ',
                ([session['seat']], [session['id']]))
    acc = cur.fetchone()
    if acc:
        last_upload = acc[2]

    global subdir
    subdir = ownpath(session['seat'], str(session['id']))

    FilePath = request.files['file']
    if FilePath and allowed_file(FilePath.filename):
        filename = secure_filename(FilePath.filename)

        if last_upload:
            os.remove(maindir + subdir + last_upload.decode())
            cur = conn.cursor()
            cur.execute("UPDATE pics SET timetable = Null WHERE seat_id = %s AND user_id = %s",
                        (session['seat'], session['id']))
            conn.commit()

        path = os.path.join(maindir, subdir)
        if not os.path.exists(path):
            os.makedirs(path)
        FilePath.save(os.path.join(maindir + subdir, filename))
        if not acc:
            cur.execute('INSERT INTO pics(timetable, seat_id, user_id) VALUES (%s, %s, %s) ',
                        (filename, [session['seat']], [session['id']]))
            conn.commit()
        else:
            cur.execute("UPDATE pics SET timetable = %s WHERE seat_id = %s AND user_id = %s",
                        (filename, [session['seat']], [session['id']]))
            conn.commit()

        return redirect(url_for('profile'))


# DISPLAY
@app.route('/display/<filename>')
def display_image(filename):
    location = ownpath(session['seat'], str(session['id']))
    return redirect(url_for('static/uploads/', filename=location + filename.decode()), code=301)


# LINE FUCTION
def push(tokens, reason, attime, duration, sender):

    def convertTuple(tup):
        count = 0
        data = ''
        for item in tup:
            if count < 2:
                data = data + item + ' '
                count += 1
            else:
                data = data + '\n' + item
        return data

    datas = convertTuple(sender)
    url = 'https://notify-api.line.me/api/notify'
    token = tokens
    headers = {
        'content-type':
        'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + token
    }
    msg = (reason + '\nณ เวลา : ' + attime + ' น.\nใช้เวลา : ' +
           duration + '\n\nส่งโดย \n' + datas)
    requests.post(url, headers=headers, data={'message': msg})


# SEARCH
@ app.route("/searchdata", methods=["POST", "GET"])
def searchdata():
    if request.method == 'POST':

        if session['seat'] == 'teacher':
            search_word = request.form['search_word']
            print(search_word)
            cur = conn.cursor()
            query = "SELECT * FROM student WHERE fname LIKE '%{}%' OR lname LIKE '%{}%' ORDER BY student_id DESC LIMIT 20".format(
                search_word, search_word)
            cur.execute(query)
            programming = cur.fetchall()
        else:
            search_word = request.form['search_word']
            print(search_word)
            cur = conn.cursor()
            query = "SELECT * FROM teacher WHERE fname LIKE '%{}%' OR lname LIKE '%{}%' ORDER BY teacher_id DESC LIMIT 20".format(
                search_word, search_word)
            cur.execute(query)
            programming = cur.fetchall()

    return jsonify({'data': render_template('response.html', programming=programming)})


# SHOW DATA
@ app.route("/")
def showData():
    if 'loggedin' in session:
        cur = conn.cursor()
        cur.execute("select * from teacher")
        record = cur.fetchall()
        return render_template('search.html')
        # return render_template('index.html', datas=record)
    else:
        return redirect(url_for('login'))
        # return render_template('login.html')


# INSERT
@ app.route("/insert", methods=['POST'])
def insertData():
    if request.method == "POST":
        email = request.form['email']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        password = request.form['password']
        # cursor = conn.cursor()
        with conn.cursor() as cursor:
            sql = "insert into teacher(email,fname,lname,phone,upassword) values(%s,%s,%s,%s,%s)"
            cursor.execute(sql, (email, fname, lname, phone, password))
            conn.commit()
        return redirect(url_for('showData'))


# UPDATE
@ app.route("/update", methods=['POST'])
def updateData():

    if request.method == "POST":
        if session['seat'] == 'teacher':
            id_update = request.form['id']
            fname = request.form['fname']
            lname = request.form['lname']
            phone = request.form['phone']
            faculty = request.form['faculty']
            sfaculty = request.form['sfaculty']
            password = request.form['password']
            token = request.form['token']

            with conn.cursor() as cursor:
                sql = "UPDATE teacher SET fname = %s, lname =%s, phone = %s, upassword = %s, faculty = %s, sfaculty = %s, token = %s WHERE teacher_id = %s"
                cursor.execute(sql, (fname, lname, phone, password,
                               faculty, sfaculty, token, id_update))
                conn.commit()

                cursor.execute(
                    'SELECT * FROM teacher WHERE teacher_id = %s', [session['id']])
                account = cursor.fetchone()
                msg = "บันทึกข้อมลเรียบร้อย"
                return redirect(url_for('profile', account=account, msg=msg))

        elif session['seat'] == 'student':
            id_update = request.form['id']
            fname = request.form['fname']
            lname = request.form['lname']
            phone = request.form['phone']
            faculty = request.form['faculty']
            sfaculty = request.form['sfaculty']
            password = request.form['password']
            token = request.form['token']

            with conn.cursor() as cursor:
                sql = "UPDATE student SET fname = %s, lname =%s, phone = %s, upassword = %s, faculty = %s, sfaculty = %s, token = %s WHERE student_id = %s"
                cursor.execute(sql, (fname, lname, phone, password,
                               faculty, sfaculty, token, id_update))
                conn.commit()

                cursor.execute(
                    'SELECT * FROM student WHERE student_id = %s', [session['id']])
                account = cursor.fetchone()
                msg = "บันทึกข้อมลเรียบร้อย"
                flash("บันทึกข้อมลเรียบร้อย")
                return redirect(url_for('profile', account=account, msg=msg))


# DELETE
@ app.route("/delete/<string:id_data>", methods=['GET'])
def delete(id_data):
    cur = conn.cursor()
    cur.execute("delete from teacher where teacher_id = %s", (id_data))
    conn.commit()
    return redirect(url_for('showData'))


# TEACHER SCHEDULE #####################################################
@ app.route("/p/<string:id_data>", methods=['GET'])
def searchprofile(id_data):

    global subdir  

    if session['seat'] == 'student':
        cur = conn.cursor()
        cur.execute("select * from teacher where teacher_id = %s", (id_data))
        record = cur.fetchone()
        subdir = ownpath('teacher', str(record[0]))


        # PIC
        cur.execute('SELECT * FROM pics WHERE seat_id = %s AND user_id = %s',
                    ('teacher', str(record[0])))
        filename = cur.fetchone()
        return render_template('schedule.html', info=record, filename=filename, maindir=maindir, subdir=subdir)
    else:
        cur = conn.cursor()
        cur.execute("select * from student where student_id = %s", (id_data))
        record = cur.fetchone()
        subdir = ownpath('student', str(record[0]))

        # PIC
        cur.execute('SELECT * FROM pics WHERE seat_id = %s AND user_id = %s',
                    ('student', str(record[0])))
        filename = cur.fetchone()
        return render_template('schedule.html', info=record, filename=filename, maindir=maindir, subdir=subdir)
 

# SEnd FORM
@ app.route("/sendline", methods=['POST'])
def sendLine():

    cur = conn.cursor()
    if session['seat'] == 'student':

        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'id' in request.form and 'reason' in request.form != "" and 'attime' in request.form != "" and 'duration' in request.form != "":

            id = request.form['id']
            reason = request.form['reason']
            attime = request.form['attime']
            duration = request.form['duration']

            # Fetch Reciever
            cur.execute('SELECT * FROM teacher WHERE teacher_id = %s', id)
            accounts = cur.fetchone()
            tokens = accounts[9]

            if attime != '' and reason != '':
                # Fetch Sender
                cur.execute('SELECT fname, lname, faculty, phone FROM student WHERE student_id = %s', [
                            session['id']])
                sender = cur.fetchone()
                push(tokens, reason, attime, duration, sender)
                return render_template('sent.html')

            return render_template('fail.html')

    else:

        if request.method == 'POST' and 'id' in request.form and 'reason' in request.form != "" and 'duration' in request.form != "":

            id = request.form['id']
            reason = request.form['reason']
            duration = request.form['duration']

            cur.execute('SELECT * FROM teacher WHERE teacher_id = %s', id)
            accounts = cur.fetchone()
            tokens = accounts[9]

            if reason != '':
                cur.execute('SELECT fname, lname, faculty, phone FROM student WHERE student_id = %s', [
                            session['id']])
                sender = cur.fetchone()
                push(tokens, reason, ' - ', duration, sender)
                return render_template('sent.html')

            return render_template('fail.html')


# CATEGORING
@ app.route("/list/<string:fac>/<string:sfac>", methods=['GET'])
def category(fac, sfac):

    if session['seat'] == 'student':
        cur = conn.cursor()
        cur.execute(
            "select * from teacher where faculty = %s AND sfaculty = %s ORDER BY fname ASC", (fac, sfac))
        record = cur.fetchall()
        return render_template('list.html', programing=record)
    else:
        cur = conn.cursor()
        cur.execute(
            "select * from student where faculty = %s AND sfaculty = %s ORDER BY fname ASC", (fac, sfac))
        record = cur.fetchall()
        return render_template('list.html', programing=record)


@ app.route("/category")
def cate():
    if 'loggedin' in session:
        return render_template('category.html')
    return render_template('login.html')


###########################################################
###########################################################
#                  LOGIN AND REGISTER                     #
###########################################################
###########################################################


# HOME
@ app.route("/home")
def userwelcome():

    return render_template('home.html')


# PROFILE PAGE
@ app.route('/profile')
def profile():
    cur = conn.cursor()
    global subdir
    if 'loggedin' in session:

        if session['seat'] == 'teacher':
            cur.execute(
                'SELECT * FROM teacher WHERE teacher_id = %s', [session['id']])
            account = cur.fetchone()

            # PIC
            cur.execute('SELECT * FROM pics WHERE seat_id = %s AND user_id = %s',
                        ([session['seat']], [session['id']]))
            filename = cur.fetchone()

            subdir = ownpath(session['seat'], str(session['id']))
            if filename:
                return render_template('profile.html', account=account, filename=filename, maindir=maindir, subdir=subdir)
            return render_template('profile.html', account=account, filename=filename)

        elif session['seat'] == 'student':
            cur.execute(
                'SELECT * FROM student WHERE student_id = %s', [session['id']])
            account = cur.fetchone()

            # PIC
            cur.execute('SELECT * FROM pics WHERE seat_id = %s AND user_id = %s',
                        ([session['seat']], [session['id']]))
            filename = cur.fetchone()
            subdir = ownpath(session['seat'], str(session['id']))
            if filename:
                return render_template('profile.html', account=account, filename=filename, maindir=maindir, subdir=subdir)
            return render_template('profile.html', account=account, filename=filename)

    return redirect(url_for('login'))


# LOGIN
@ app.route('/login', methods=['GET', 'POST'])
def login():

    if 'loggedin' not in session:

        cur = conn.cursor()
        msg = ''
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']

            # Check if account exists using MySQL
            cur.execute(
                'SELECT * FROM teacher WHERE email = %s AND upassword = %s', (email, password))
            account = cur.fetchone()
            cur.execute(
                'SELECT * FROM student WHERE email = %s AND upassword = %s', (email, password))
            account2 = cur.fetchone()

            # If account exists in accounts table in our database
            if account:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account[0]
                session['email'] = account[1]
                session['seat'] = account[6]
                # Redirect to home page
                # return 'Logged in successfully!'
                return render_template('search.html')

            elif account2:
                cur.execute(
                    'SELECT * FROM student WHERE email = %s AND upassword = %s', (email, password))
                account = cur.fetchone()
                session['loggedin'] = True
                session['id'] = account2[0]
                session['email'] = account2[1]
                session['seat'] = account2[6]
                # Redirect to home page
                # return 'Logged in successfully!'
                return render_template('search.html')
            else:
                msg = 'Incorrect email/password!'

        return render_template('login.html', msg=msg)

    return render_template('search.html')


# REGISTER
@ app.route('/register', methods=['GET', 'POST'])
def register():
    cur = conn.cursor()

    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'fname' in request.form and 'lname' in request.form and 'seat' in request.form and 'faculty' in request.form:
        # Create variables for easy access
        email = request.form['email']
        fname = request.form['fname']
        lname = request.form['lname']
        password = request.form['password']
        faculty = request.form['faculty']
        seat = request.form['seat']

        # Check if account exists using MySQL
        cur.execute('SELECT * FROM teacher WHERE email = %s', (email))
        account = cur.fetchone()

        cur.execute('SELECT * FROM student WHERE email = %s', (email))
        account2 = cur.fetchone()

        # If account exists show error and validation checks
        if account:
            msg = 'Email already exists!'
        elif account2:
            msg = 'Email already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid, Please fill out the form'
        elif not email or not fname or not lname or not password or not seat or not faculty:
            msg = 'Please fill out the form!'
        else:
            if seat == 'teacher':
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                cur.execute('INSERT INTO teacher (email, fname, lname, upassword, seat, faculty) VALUES (%s, %s, %s, %s, %s, %s)',
                            (email, fname, lname, password, seat, faculty))
                conn.commit()
                msg = 'You have successfully registered!'
                return render_template('login.html', msg=msg)

            elif seat == 'student':
                cur.execute('INSERT INTO student (email, fname, lname, upassword, seat, faculty) VALUES (%s, %s, %s, %s, %s, %s)',
                            (email, fname, lname, password, seat, faculty))
                conn.commit()
                msg = 'You have successfully registered!'
                return render_template('login.html', msg=msg)

    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


# Log out
@ app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    session.pop('seat', None)
    global subdir
    subdir = ''
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
