import datetime
from app import db
from sqlalchemy import or_, and_, delete, desc, asc
from datetime import datetime

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
    desc = db.Column(db.Text , nullable=False)
    email = db.Column(db.String(50))
    role = db.Column(db.String(20))
    id_channel = db.Column(db.String(50), nullable=False)
    pay_rate = db.Column(db.String(150), nullable=False)
    pic = db.Column(db.Text)

    def __repr__(self):
        return '<User id: {self.id}, username: {self.username}, password: {self.password}, fullname: {self.fullname}, desc: {self.desc}, email: {self.email},role: {self.role},  id_channel: {self.id_channel}, pay_rate: {self.pay_rate}, pic: {self.pic}>'
 

chatrooms = db.Table('chatrooms',
                    db.Column('id', db.Integer, primary_key=True),
                    db.Column('my_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('ur_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('room_id', db.String(100)),

                    db.Column('user_name', db.String(100)),
                    db.Column('room_message', db.String(255)),
                    db.Column('flag', db.String(10)),
                    db.Column('user_pic', db.Text),
                    db.Column('date_time', db.DateTime, default=datetime.now())
                    )


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chatroom = db.Column(db.String(200))
    sender_id = db.Column(db.String(100))
    message = db.Column(db.String(255))
    pic = db.Column(db.Text) 
    date_time = db.Column(db.DateTime, default=datetime.now()) 

    def __repr__(self):
        return '<Chat id: {self.id}, chatroom: {self.chatroom} , sender_id: {self.sender_id} , chatroom: {self.chatroom} , message: {self.message}, date_time: {self.date_time}, pic: {self.pic}>'
