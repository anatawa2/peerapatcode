from flask import Blueprint
from flask import render_template, request, flash, session, url_for, redirect

from views import Conn

users = Blueprint('users', __name__, template_folder='templates')


# INDEX
@users.route('/')
def index():

    if 'loggedin' not in session:
        session['temp'] = ''
        return render_template('/login.html')

    return render_template('/index.html')


# SELECT ROLE
@users.route('/register', methods=['GET'])
def register():
    session['temp'] = ''
    return render_template('/register.html')


# ROLE
@users.route('/register/<string:choice>', methods=['GET'])
def usersRegister(choice='NO'):

    if choice == 'youtuber':
        # TRIGGER TYPE
        session['temp'] = 'yt'
        return render_template('/registerform.html')

    elif choice == 'sponsor':
        return render_template('/registerform.html')

    return render_template('/register.html')


# REGISTED
@users.route('/registed', methods=['POST'])
def tosubmit():
    error = None
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        phone = request.form['phone']
        status = request.form['status']
        check =  Conn.toCheck(username)
        if not username or not password or not fullname or not phone:
            error = 'Fill out the form'

        # check if account already exists
        if username == check.username:
            error = 'Username already exists!'    

        if error is None:
            Conn.toRegister(username, password, fullname, phone, status)
            msg = 'Register done!'
            return render_template('/login.html', msg=msg)

        flash(error)

    return render_template('/registerform.html',)


# LOGIN
@users.route('/login', methods=['GET', 'POST'])
def login():

    if 'loggedin' not in session:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            error = None
            User = Conn.toLogin(username, password)

            if not username or not password:
                error = 'Fill out the form'

            if User is None:
                error = 'Incorrect username.'

            elif error is None:
                print(User)
                session['id'] = User.id
                session['loggedin'] = True
                return render_template('/index.html')

            flash(error)

        return redirect(url_for('users.index'))

    return render_template('/index.html')


# LOGOUT
@users.route('/logout')
def logout():
    session.clear()
    return render_template('/login.html')
