import os
from re import X
from flask import render_template, request, flash, session, url_for, redirect
from views import *
from flask.views import View
from werkzeug.utils import secure_filename
from googleapiclient.discovery import build



class MyProfile(View):
    def dispatch_request(self):
        if 'loggedin' in session:
            me = session['id']
            profile = Conn.toProfile(me)
            tags = Style.showTag(me)
            img = Conn.getImg(me)           

            return render_template('/profile.html', data=profile, tag=tags, img=img)

        return render_template('/login.html')


class UpdateProfile(View):
    def dispatch_request(self):
        if request.method == "POST":
            a = request.form['id']
            b = request.form['fullname']
            c = request.form['desc']
            d = request.form['email']
            e = request.form['password']
            f = request.form['payrate']
            updated = Conn.toUpdate(a, b, c, d, e, f)
            flash('Updated')
        return redirect(url_for('profile', data=updated))

    def uploadIMG():
        if request.method == "POST":
            FilePath = request.files['file']
            if not FilePath:
                return 'No pic uploaded!', 400

            filename = secure_filename(FilePath.filename)
            if not filename:
                return 'Bad upload!', 400

        last_upload = ''         
        maindir = 'static/uploads/'
        owner = str(session['id'])
        img = db.session.query(Img).filter(Img.owner == owner).first()


        if img:
            last_upload = img.name

        if last_upload:
            os.remove(maindir + owner + '/' + last_upload) 
            drop = delete(Img).where(Img.owner == owner)
            db.session.execute(drop)
            db.session.commit()

        path = os.path.join(maindir, owner + '/')

        if not os.path.exists(path):
            os.makedirs(path)

        FilePath.save(os.path.join(maindir + owner + '/', filename))
        updated = Conn.uploadImg(owner, filename)
      

        flash('Updated')
        return redirect(url_for('profile', img=updated))


# UPDATE USER TAG

class SaveTag(View):
    def dispatch_request(self):
        if request.method == "POST":
            id = request.form['id']
            select = request.form.getlist('checkbox')
            Style.setTag(id, select)

            return redirect(url_for('profile'))


# Search By Tag
class SearchByTag(View):
    def dispatch_request(self):
        return render_template('tag.html')

    def getTag(tag):
        tagID = which(tag)
        users = Style.byTag(tagID)
        # if no data
        if users == []:
            users = "nothing"

        return render_template('tagresult.html', data=users)


class Recommended(View):
    def dispatch_request(self):
        # HOME PAGE
        users = Style.byTag(1)
        APIs = Visit.fetchID("UCuTTT_6JxuAtRdvF3BvVjdg")
        return render_template('recommended.html', data=users, APIs=APIs)


class Visit(View):

    # /visit/<id>
    def VisitTo(id):
        user = Conn.toProfile(id)
        x = Visit.fetchID("UCuTTT_6JxuAtRdvF3BvVjdg")
        return render_template('visit.html', data=user, APIs=x)

    # API
    def fetchID(channelID):
        api_key = "AIzaSyChexdcc_Ucu8qQUlFZyXDbhfiiCIFfS-A"
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.channels().list(
            part="statistics,snippet",
            id=channelID
        )
        response = request.execute()

        # FETCH API
        titleChannel = response["items"][0]["snippet"]["localized"]["title"]
        subscriberCount = format(
            int(response["items"][0]["statistics"]["subscriberCount"]), ",")

        viewCount = format(
            int(response["items"][0]["statistics"]["viewCount"]), ",")
        videoCount = format(
            int(response["items"][0]["statistics"]["videoCount"]), ",")

        publishedAt = response["items"][0]["snippet"]["publishedAt"]
        lang = response["items"][0]["snippet"]["country"]
        pic = response["items"][0]["snippet"]["thumbnails"]["high"]["url"]

        return [titleChannel, subscriberCount, viewCount, videoCount, publishedAt, lang, pic]

        # return render_template('visit.html', titleChannel=titleChannel,
        #                        subscriberCount=subscriberCount,
        #                        viewCount=viewCount,
        #                        videoCount=videoCount,
        #                        publishedAt=publishedAt,
        #                        lang=lang, pic=pic,)


# SEARCH
class SearchProfile(View):
    def dispatch_request(self):

        name = request.form["name"]
        search = "%{}%".format(name)
        record = db.session.query.filter(User.fullname.like(search)).all()

        return render_template('search.html', record = record)
