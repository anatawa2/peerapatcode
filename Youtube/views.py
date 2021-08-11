from app import app, db
from models import *

# @app.route('/')
# def index():
#      return 'hello'


class Conn():

    def toCheck(a):
        username = db.session.query(User).filter(User.username == a).first()
        return username

    def toLogin(a, b):
        username = db.session.query(User).filter(and_(User.username == a, User.password == b)).first()
        return username

    def toRegister(a, b, c, d, e):
        user = User(username=a, password=b, fullname=c, phone=d, status=e)
        db.session.add(user)
        db.session.commit()

    def toProfile(a):
        profile = db.session.query(User).filter(User.id == a).first()
        return profile

    def toUpdate(a, b, c, d, e):
        updated = db.session.query(User).filter(User.id == a).first()
        updated.fullname = b
        updated.desc = c
        updated.phone = d
        updated.password = e
        db.session.commit()
