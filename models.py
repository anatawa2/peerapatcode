
from app import db
from sqlalchemy import or_, and_, delete

style = db.Table('style',
                 db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'))                 
                 )


class Tag(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(30))
    tagging = db.relationship('User', secondary=style)

    def __repr__(self):
        return '<Tag id: {self.id}, tag_name: {self.tag_name}>'


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100))
    fullname = db.Column(db.String(100))
    desc = db.Column(db.Text)
    role = db.Column(db.String(20))
    pay_rate = db.Column(db.String(150))
    tag = db.Column(db.String(200))
    email = db.Column(db.String(50))

    def __repr__(self):
        return '<User id: {self.id}, username: {self.username}, password: {self.password}, fullname: {self.fullname}, desc: {self.desc}, phone: {self.phone}, pay_rate: {self.pay_rate}, role: {self.role},  tag: {self.tag}>'




class Img(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, nullable=False) 
    name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<User id: {self.id}, owner: {self.owner}, name: {self.name}>'