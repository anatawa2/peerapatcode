
from app import db
from sqlalchemy import or_, and_

style = db.Table('style',
                 db.Column('tag_id', db.Integer, db.ForeignKey('tag.tag_id')),
                 db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'))                 
                 )


class Tag(db.Model):

    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(30))
    tagging = db.relationship('User', secondary=style)

    def __repr__(self):
        return '<Tag tag_id: {self.tag_id}, tag_name: {self.tag_name}>'


class User(db.Model):

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100))
    fullname = db.Column(db.String(100))
    desc = db.Column(db.Text)
    role = db.Column(db.String(20))
    phone = db.Column(db.Integer)
    pay_rate = db.Column(db.String(150))
    tag = db.Column(db.String(200))

    def __repr__(self):
        return '<User user_id: {self.user_id}, username: {self.username}, password: {self.password}, fullname: {self.fullname}, desc: {self.desc}, phone: {self.phone}, pay_rate: {self.pay_rate}, role: {self.role},  tag: {self.tag}>'
