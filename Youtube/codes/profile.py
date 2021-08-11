from flask import Blueprint
from flask import render_template, request, flash, session , url_for, redirect

from views import Conn

profile = Blueprint('profile', __name__, template_folder='templates')


# PROFILE
@profile.route('/')
def myProfile():

    if 'loggedin' in session:
        profile = Conn.toProfile(session['id'])
        session['status'] = profile.status
        return render_template('/profile.html', data=profile)

    return render_template('/login.html')


# UPDATE PROFILE
@profile.route('/update', methods=['POST'])
def myUpdate():

    if request.method == "POST":
        a  = request.form['id']
        b = request.form['fullname']
        c = request.form['desc']
        d = request.form['phone']
        e = request.form['password']
        updated = Conn.toUpdate(a,b,c,d,e)
        flash('Updated')
        return redirect(url_for('profile.myProfile', data = updated))


# SEARCH 
@profile.route('/search', methods=['GET'])
def search():
    return render_template('search.html')



# TAG
@profile.route('/tag', methods=['GET'])
def tag():
    return render_template('tag.html')