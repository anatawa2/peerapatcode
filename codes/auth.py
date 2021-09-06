from flask import render_template, request, flash, session, url_for, redirect
from flask.views import View
from views import *
from models import *


class IndexView(View):
    def dispatch_request(self):
        if 'loggedin' not in session:
            session['temp'] = ''
            return render_template('/login.html')

        return redirect(url_for('recommended'))
        # return render_template('/index.html')


class RoleRegister(View):
    def dispatch_request(self):
        session['temp'] = ''
        return render_template('/register.html')

    def pick_role(role):
        if role == 'youtuber':
            # TRIGGER ROLE
            session['temp'] = 'yt'
            return render_template('/registerform.html')

        elif role == 'sponsor':
            return render_template('/registerform.html')

        return render_template('/register.html')

    def submit_role():
        error = None
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            repassword = request.form['repassword']
            fullname = request.form['fullname']
            email = request.form['email']
            role = request.form['role']
            check = Conn.toCheck(username)
            check2 = Conn.toCheck(email)

            if not username or not password or not repassword or not fullname or not email:
                error = 'Fill out the form'

            if check:
                error = 'Username already exist!'
            
            if check2:
                error = 'Email already used!'

            if password != repassword:
                error = "Password and re-password don't match"

            if error is None:
                Conn.toRegister(username, password, fullname, email, role)
                flash('Register done!')
                return redirect(url_for('index'))

            flash(error)

        return render_template('/registerform.html',password=password,repassword=repassword)


class LoginForm(View):
    def dispatch_request(self):

        if 'loggedin' not in session:
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']

                try:
                    if request.form['remember']:
                        remember = True
                except:
                    remember = False
 
                error = None
                user = Conn.toLogin(username, password)

                if not username or not password:
                    error = 'Fill out the form'

                elif user is None:
                    error = 'Incorrect User or Password.'

                elif error is None:
                    session['id'] = user.id
                    session['role'] = user.role
                    session['loggedin'] = True
                    session.permanent = remember

                    return redirect(url_for('recommended'))

                flash(error) 

            return redirect(url_for('index'))

        return render_template('/index.html')

    def logout():
        session.clear()
        session.permanent = False
        return render_template('/login.html')
