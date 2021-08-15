from flask import Blueprint
from flask import render_template, request, flash, session, url_for, redirect
from sqlalchemy.sql.expression import null
from flask.views import View
from views import Conn


class IndexView(View):
    def dispatch_request(self):
        if 'loggedin' not in session:
            session['temp'] = ''
            return render_template('/login.html')

        return render_template('/index.html')


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
            fullname = request.form['fullname']
            phone = request.form['phone']
            role = request.form['role']
            check = Conn.toCheck(username)

            if not username or not password or not fullname or not phone:
                error = 'Fill out the form'

            if check:
                error = 'Username already exists!'

            if error is None:
                Conn.toRegister(username, password, fullname, phone, role)
                flash('Register done!')
                return redirect(url_for('index'))

            flash(check)

        return render_template('/registerform.html',)


class LoginForm(View):
    def dispatch_request(self):

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
                    session['id'] = User.id
                    session['loggedin'] = True
                    return render_template('/index.html')

                flash(error)

            return redirect(url_for('index'))

        return render_template('/index.html')
        
    def logout():
        session.clear()
        return render_template('/login.html')


