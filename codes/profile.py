from flask import Blueprint
from flask import render_template, request, flash, session, url_for, redirect
from views import Conn
from flask.views import View


class MyProfile(View):
    def dispatch_request(self):
        if 'loggedin' in session:
            profile = Conn.toProfile(session['id'])
            session['role'] = profile.role

            return render_template('/profile.html', data=profile)

        return render_template('/login.html')


class UpdateProfile(View):
    def dispatch_request(self):
        if request.method == "POST":
            a = request.form['id']
            b = request.form['fullname']
            c = request.form['desc']
            d = request.form['phone']
            e = request.form['password']
            updated = Conn.toUpdate(a, b, c, d, e)
            flash('Updated')
        return redirect(url_for('profile', data=updated))


class SearchProfile(View):    
    def dispatch_request(self):
        return render_template('search.html')


class SearchByTag(View):    
    def dispatch_request(self):
        return render_template('tag.html')

class visit(View):
    def dispatch_request(self):

        return render_template('visit.html', )
        
