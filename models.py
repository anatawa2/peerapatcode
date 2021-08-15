from sqlalchemy.sql.elements import Null
from app import db
from sqlalchemy import or_, and_


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)

    def __repr__(self):
        return '<Post id: {self.id}, title: {self.title}, body: {self.body}>'


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100))
    fullname = db.Column(db.String(100))
    desc = db.Column(db.Text)
    role = db.Column(db.String(20))
    phone = db.Column(db.Integer)
    pay_rate = db.Column(db.String(150))
    tag = db.Column(db.String(200))

    def __repr__(self):
        return '<User id: {self.id}, username: {self.username}, password: {self.password}, fullname: {self.fullname}, desc: {self.desc}, phone: {self.phone}, pay_rate: {self.pay_rate}, role: {self.role},  tag: {self.tag}>'
