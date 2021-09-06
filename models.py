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
    email = db.Column(db.String(50))
    role = db.Column(db.String(20))
    id_channel = db.Column(db.String(50))
    pay_rate = db.Column(db.String(150))
    pic = db.Column(db.Text)

    def __repr__(self):
        return '<User id: {self.id}, username: {self.username}, password: {self.password}, fullname: {self.fullname}, desc: {self.desc}, email: {self.email},role: {self.role},  id_channel: {self.id_channel}, pay_rate: {self.pay_rate}, pic: {self.pic}>'

 


