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
        username = db.session.query(User).filter(
            and_(User.username == a, User.password == b)).first()
        return username

    def toRegister(a, b, c, d, e):
        user = User(username=a, password=b, fullname=c, phone=d, role=e)
        db.session.add(user)
        db.session.commit()

    def toProfile(a):
        profile = db.session.query(User).filter(User.id == a).first()
        return profile

    def toUpdate(a, b, c, d, e, f):
        updated = db.session.query(User).filter(User.id == a).first()
        updated.fullname = b
        updated.desc = c
        updated.email = d
        updated.password = e
        updated.pay_rate = f
        db.session.commit()

    def uploadImg(a, b,):
        stmt = Img(owner=a, name=b)
        db.session.add(stmt)
        db.session.commit()

        # img = db.session.query(Img).filter(Img.owner == a).first()
        # return img
    
    def getImg(me):
        maindir = 'static/uploads'
        owner = str(me)
        img = db.session.query(Img).filter(Img.owner == me).first()

        return [maindir,owner,img]
 


class Style():
    # selectTag = ['Entertainment', 'History']
    def setTag(ID, selectTag):

        for count in range(23):
            stmt2 = (delete(style).where(style.c.user_id == ID, style.c.tag_id == count+1))
            db.session.execute(stmt2)
            db.session.commit()

        for tag in selectTag:
            keyid = which(tag)
            stmt1 = style.insert().values(user_id=ID, tag_id=keyid)
            db.session.execute(stmt1)
            db.session.commit()

    # SHOW CHECKBOX

    def showTag(a):
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


# TAG position
# input =  [1,2,3,4]
def posTag(input):
    temp = [0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
    for x in input:
        temp[x] = 1
    return temp


# convert tag_name to tag_id
def which(style):
    for k, v in datas.items():
        if style == k:
            return v


# TAG
global datas
datas = {
    "Entertainment": 1,
    "Family": 2,
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
    "NEWS": 19,
    "Podcast": 20,

    "Motivation": 21,
    "History": 22
}
