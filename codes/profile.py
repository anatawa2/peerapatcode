import os
from flask import render_template, request, flash, session, url_for, redirect
from views import *
from flask.views import View
from werkzeug.utils import secure_filename
from googleapiclient.discovery import build
import random


class MyProfile(View):
    def dispatch_request(self):
        if 'loggedin' in session:
            me = session['id']
            profile = Conn.toProfile(me)
            tags = Style.showPos(me)
            show = Style.showTag(me)
            api = ''

            if session['role'] == 'youtuber':
                try:
                    api = APIs.ID(profile.id_channel)
                except:
                    api = ''

            return render_template('/profile.html', data=profile, tag=tags, api=api, showtag=show, profilepage=True)

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

            if request.files['file']:
                UpdateProfile.uploadIMG()

            if session['role'] == "youtuber":
                g = request.form['pic']
                h = request.form['id_channel']
                updated = Conn.toUpdateYT(a, b, c, d, e, f, g, h)
            else:
                updated = Conn.toUpdateSP(a, b, c, d, e, f)

            flash('UPDATED')
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
        me = str(session['id'])
        user = Conn.toProfile(me)

        if user:
            last_upload = user.pic

        if last_upload:
            os.remove(maindir + me + '/' + last_upload)

        path = os.path.join(maindir, me + '/')

        if not os.path.exists(path):
            os.makedirs(path)

        FilePath.save(os.path.join(maindir + me + '/', filename))
        updated = Conn.uploadImg(me, filename)

        # flash('Updated')
        return redirect(url_for('profile', img=updated))


# UPDATE USER TAG

class SaveTag(View):
    def dispatch_request(self):
        if request.method == "POST":
            id = request.form['id']
            select = request.form.getlist('checkbox')
            # Save
            Style.setTag(id, select)

            return redirect(url_for('profile'))


# Search By Tag
class SearchByTag(View):
    def dispatch_request(self):
        return render_template('tag.html', tagpage=True)

    def getTag(tag):

        tagID = name2id(tag)
        users = Style.byTag(tagID)

        tags,fetch = [],[]
        for i in range(len(users)):

            b = Style.showTag(users[i].id)
            tags.append(b)

            if session['role'] == "sponsor":
                a = APIs.ID(users[i].id_channel)
                fetch.append(a)

        return render_template('result.html', datas=users, fetch=fetch, tags=tags, title=tag, tagpage=True)


# HOME PAGE
class Recommended(View):
    def dispatch_request(self):

        if session['role'] == "youtuber":
            users = db.session.query(User).filter(User.role == "sponsor").all()
            random.shuffle(users)
            title = "บริษัทที่คุณอาจสนใจ"
        else:
            users = db.session.query(User).filter(
                User.role == "youtuber").all()
            random.shuffle(users)
            title = "แชนแนลที่คุณอาจสนใจ"

        indx,tags,fetch = [],[],[]  # [obj,obj,obj] 
        for i in range(5):
            indx.append(users[i])

            b = Style.showTag(users[i].id)
            tags.append(b)

            if session['role'] == "sponsor":
                a = APIs.ID(users[i].id_channel)
                fetch.append(a)

        return render_template('result.html', datas=indx, fetch=fetch, tags=tags, title=title , homepage=True)


# USER PROFILE
class Visit(View):

    # /visit/<id>
    def VisitTo(id):
        user = Conn.toProfile(id)
        tags = Style.showTag(id)

        fetch = APIs.ID(user.id_channel)
        vdo = APIs.vdo(user.id_channel)
        return render_template('visit.html', data=user, tags=tags, api=fetch, vdo=vdo)


# SEARCH
class SearchProfile(View):
    def dispatch_request(self):
        if request.method == "POST":
            name = request.form['search']
            title = ('ผลการค้นหา : ' + name)
            search = "%{}%".format(name)

            if session['role'] == "youtuber":
                users = db.session.query(User).filter(
                    and_(User.fullname.like(search), User.role == "sponsor")).all()
            else:
                users = db.session.query(User).filter(
                    and_(User.fullname.like(search), User.role == "youtuber")).all()

            tags,fetch = [],[]
            for i in range(len(users)):

                b = Style.showTag(users[i].id)
                tags.append(b)

                if session['role'] == "sponsor":
                    a = APIs.ID(users[i].id_channel)
                    fetch.append(a)

        return render_template('result.html', datas=users, fetch=fetch, tags=tags, title=title, searchpage=True)

    def searchName():

        return render_template('search.html', searchpage=True)


class APIs(View):
    # API
    def ID(channelID):
        api_key = "AIzaSyAae50fLK2RJv8DDJg93SX08H0uEPCiuuU"
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

        a = response["items"][0]["snippet"]["publishedAt"]
        publishedAt = ('%.10s' % a)

        pic = response["items"][0]["snippet"]["thumbnails"]["high"]["url"]

        return [titleChannel, subscriberCount, viewCount, videoCount, publishedAt, pic]

    # API VIDEO

    def vdo(channelID):
        api_key = "AIzaSyBcS6kuesLl9bin3DZMaTV0zUwaWWQbVxY"
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.search().list(
            part="snippet",
            channelId=channelID,
            order="date",
        )
        response = request.execute()
        vidId = response["items"][0]["id"]["videoId"]
        vidTitle = response["items"][0]["snippet"]["title"]
        vidPic = response["items"][0]["snippet"]["thumbnails"]["high"]["url"]

        return [vidId, vidTitle, vidPic]


# {{vdo[count.value][1]}}
# <div class="card">
#     <a data-fancybox href="https://www.youtube.com/watch?v={{vdo[count.value][0]}}">
#         <img src="{{vdo[count.value][2]}}" alt="pic" style="max-width: 10%">
#     </a>
# </div>
