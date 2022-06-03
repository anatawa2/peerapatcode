from flask import render_template, session
from app import *
from models import *


# @app.route('/')
# def index():
#      return 'hello'


class Conn():

    def toCheck(a):
        username = db.session.query(User).filter(
            or_(User.username == a, User.email == a)).first()
        return username

    def toLogin(a, b):
        username = db.session.query(User).filter(
            and_(or_(User.username == a, User.email == a), User.password == b)).first()
        return username

    def toRegister(a, b, c, d, e):
        user = User(username=a, password=b, fullname=c, email=d, role=e ,desc='',id_channel ='',pay_rate='')
        db.session.add(user)
        db.session.commit()

    def toProfile(a):
        profile = db.session.query(User).filter(User.id == a).first()
        return profile

    def toUpdateYT(a, b, c, d, e, f, g):
        updated = db.session.query(User).filter(User.id == a).first()
        updated.fullname = b
        updated.desc = c
        updated.email = d
        updated.password = e
        updated.pay_rate = f
        updated.id_channel = g

        qry = db.session.query(Chat).filter(User.username == a).all()
        for i in qry:
            i.pic = g

        db.session.commit()

    def toUpdateSP(a, b, c, d, e, f):
        updated = db.session.query(User).filter(User.id == a).first()
        updated.fullname = b
        updated.desc = c
        updated.email = d
        updated.password = e
        updated.pay_rate = f
        db.session.commit()

    def toSearch(a):
        fullname = db.session.query(User).filter(User.fullname == a).first()
        return fullname

    def uploadImg(a, b):
        user = db.session.query(User).filter(User.id == a).first()
        user.pic = b
        db.session.commit()

        return user

    def showNotify(a):
        inbox = db.session.query(chatrooms).filter(
            chatrooms.c.my_id == a).all()

        notify = 0
        for i in inbox:
            if i.flag == '0':
                notify += 1
        
        return notify 


class Style():
    # selectTag = ['Entertainment', 'History']
    def setTag(ID, selectTag):

        # reset ALL TAG = 0
        for count in range(27):
            stmt1 = (delete(style).where(
                style.c.user_id == ID, style.c.tag_id == count+1))
            db.session.execute(stmt1)
            db.session.commit()

        for tag in selectTag:
            keyid = name2id(tag)
            stmt2 = style.insert().values(user_id=ID, tag_id=keyid)
            db.session.execute(stmt2)
            db.session.commit()

    # SHOW CHECKBOX

    def showPos(a):
        stmt = db.session.query(style).filter(style.c.user_id == a).all()
        data = []
        for tag in stmt:
            add = tag[0]
            data.append(add)
        Tags = posTag(data)
        return Tags

    # find User by tag_id

    def byTag(a):
        data = db.session.query(User).join(
            style).filter(style.c.tag_id == a).all()
        return data

    def showTag(id):
        tags = []
        pos = Style.showPos(id)  # [1,0,1,0,1]
        style = posToId(pos)     # [1,3,5]

        for i in style:
            x = id2name(i)
            tags.append(x)
        return tags              # ['Entertainment','Education','Travel']
 



# TAG position
# input =  [1,2,3,4]
def posTag(input):
    position = [0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
                0, 0, 0]
    for x in input:
        position[x] = 1
    return position


# convert tag_name to tag_id
def name2id(style):
    for k, v in datas.items():
        if style == k:
            return v  # [1 ,6]

# convert tag_id to tag_name


def id2name(style):
    for k, v in datas.items():
        if style == v:
            return k  # ["Enteraintment" ,"Kids"]


def posToId(input):   # [1,0,1,0,1]
    c = 0
    data = []
    for i in input:
        if i == 1:
            data.append(c)
        c += 1

    return data       # [1,3,5]


# TAG
global datas
datas = {
    "Entertainment": 1,
    "Health": 2,
    "Education": 3,
    "Lifestyle": 4,
    "Travel": 5,

    "Kids": 6,
    "Review": 7,
    "Tech": 8,
    "Movie": 9,
    "Animation": 10,

    "Music": 11,
    "ASMR": 12,
    "Food": 13,
    "Sport": 14,
    "Game": 15,

    "Beauty": 16,
    "Gossip": 17,
    "DIY": 18,
    "Art": 19,
    "Podcast": 20,

    "Motivation": 21,
    "History": 22,
    "Science": 23,
    "NEWS": 24,
    "Product": 25,

    "Service": 26
}
