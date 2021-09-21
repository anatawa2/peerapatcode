import os
import requests
from flask import render_template, request, flash, session, url_for, redirect
from views import *
from flask.views import View
from werkzeug.utils import secure_filename
from googleapiclient.discovery import build
import random
from datetime import datetime


class MyProfile(View):
    def dispatch_request(self):
        if 'loggedin' in session:
            me = session['id']
            profile = Conn.toProfile(me)
            notify = Conn.showNotify(me)
            tags = Style.showPos(me)
            show = Style.showTag(me)
            api = ''        
            
            if session['role'] == 'youtuber':
                try:
                    api = APIs.ID(profile.id_channel)
                except:
                    api = ''

            return render_template('/profile.html', data=profile, tag=tags, api=api, showtag=show, notify=notify , profilepage=True)

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

            if session['role'] == "youtuber":
                # save img
                pic = request.form['pic']
                try:
                    UpdateProfile.uploadIMG2(pic)
                except:
                    pass

                g = request.form['id_channel']
                updated = Conn.toUpdateYT(a, b, c, d, e, f, g)

            else:
                try:
                    UpdateProfile.uploadIMG()
                    print('save')
                except:
                    pass
                    print('fail')

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
            os.remove(last_upload[1:])

        path = os.path.join(maindir, me + '/')

        if not os.path.exists(path):
            os.makedirs(path)

        FilePath.save(os.path.join(maindir + me + '/', filename))
        updated = Conn.uploadImg(
            me, ('/static/uploads/' + str(me) + '/' + filename)) 

        # flash('Updated')
        return redirect(url_for('profile', img=updated))

    def uploadIMG2(pic):

        me = str(session['id'])

        r = requests.get(pic)

        last_upload = ''
        maindir = 'static/uploads/'
        user = Conn.toProfile(me)

        if user:
            last_upload = user.pic

        if last_upload:
            user.pic = ''
            db.session.commit()

        path = os.path.join(maindir, me + '/')

        if not os.path.exists(path):
            os.makedirs(path)

        save_path = maindir + me
        file_name = me + session['role'] + '.jpg'

        completeName = os.path.join(save_path, file_name)

        with open(completeName, "wb") as file:
            file.write(r.content)

        updated = Conn.uploadImg(me, ('/' + maindir + me + '/' + file_name))

        return redirect(url_for('profile'))


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
        notify = Conn.showNotify(session['id'])
        return render_template('tag.html', notify=notify ,tagpage=True)


    def getTag(tag):

        notify = Conn.showNotify(session['id'])
        tagID = name2id(tag)
        users = Style.byTag(tagID)

        tags, fetch = [], []
        for i in range(len(users)):

            b = Style.showTag(users[i].id)
            tags.append(b)

            if session['role'] == "sponsor":
                a = APIs.ID(users[i].id_channel)
                fetch.append(a)

        return render_template('result.html', notify=notify , datas=users, fetch=fetch, tags=tags, title=tag, tagpage=True)


# HOME PAGE
class Recommended(View):
    def dispatch_request(self):
 
        notify = Conn.showNotify(session['id'])

        if 'loggedin' not in session:
            session['temp'] = ''
            return render_template('/login.html')

        if session['role'] == "youtuber":
            users = db.session.query(User).filter(User.role == "sponsor").all()
            random.shuffle(users)
            title = "บริษัทที่คุณอาจสนใจ"
        else:
            users = db.session.query(User).filter(
                User.role == "youtuber").all()
            random.shuffle(users)
            title = "แชนแนลที่คุณอาจสนใจ"

        indx, tags, fetch = [], [], []  # [obj,obj,obj]
        for i in range(10):
            indx.append(users[i])

            b = Style.showTag(users[i].id)
            tags.append(b)

            if session['role'] == "sponsor":
                a = APIs.ID(users[i].id_channel)
                fetch.append(a)

        return render_template('result.html', notify=notify, datas=indx, fetch=fetch, tags=tags, title=title, homepage=True)


# USER PROFILE
class Visit(View):

    # /visit/<id>
    def VisitTo(id):
        notify = Conn.showNotify(session['id'])
        user = Conn.toProfile(id)
        tags = Style.showTag(id)

        fetch = APIs.ID(user.id_channel)
        o = fetch[4] 
        a = o[8:]
        b = o[5:7]
        c = o [:4]
        date = a + ' / ' + b + ' / ' + c 


        vdo = APIs.vdo(user.id_channel)

        viewCount, likeCount, dislikeCount = [], [], []
        for i in range(10):

            a = APIs.statistics(vdo[i][0])
            viewCount.append(a[0])
            likeCount.append(a[1])
            dislikeCount.append(a[2])

        # vdo = [12, 121, 12, 12, 12, 454]
        # viewCount = [10000, 200000, 345540, 400000, 500000,
        #              600000, 700000, 800000, 900000, 1000000]
        # likeCount = [1000, 20000, 34550, 40000,
        #              50000, 60000, 70000, 80000, 90000, 100000]
        # dislikeCount = [100, 2000, 3450, 4000,
        #                 5000, 6000, 7000, 8000, 9000, 10000]

        vdo.reverse()
        viewCount.reverse()
        likeCount.reverse()
        dislikeCount.reverse()

        return render_template('visit.html', date=date, notify=notify, data=user, tags=tags, api=fetch, vdos=vdo, views=viewCount, likes=likeCount, dislikes=dislikeCount, searchpage=True)


# SEARCH
class SearchProfile(View):
    def dispatch_request(self):
        if request.method == "POST":
            notify = Conn.showNotify(session['id'])
            name = request.form['search']
            title = ('ผลการค้นหา : ' + name)
            search = "%{}%".format(name)

            if not name:
                return render_template('search.html')

            if session['role'] == "youtuber":
                users = db.session.query(User).filter(
                    and_(User.fullname.like(search), User.role == "sponsor")).all()
            else:
                users = db.session.query(User).filter(
                    and_(User.fullname.like(search), User.role == "youtuber")).all()

            tags, fetch = [], []
            for i in range(len(users)):

                b = Style.showTag(users[i].id)
                tags.append(b)

                if session['role'] == "sponsor":
                    a = APIs.ID(users[i].id_channel)
                    fetch.append(a)

        return render_template('result.html',notify=notify, datas=users, fetch=fetch, tags=tags, title=title, searchpage=True)

    def searchName():
        notify = Conn.showNotify(session['id'])

        return render_template('search.html', notify=notify, searchpage=True)


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

    # API SEARCH VIDEO

    def vdo(channelID):
        # me       AIzaSyBcS6kuesLl9bin3DZMaTV0zUwaWWQbVxY
        # rmuti    AIzaSyAae50fLK2RJv8DDJg93SX08H0uEPCiuuU

        api_key = "AIzaSyAae50fLK2RJv8DDJg93SX08H0uEPCiuuU"
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.search().list(
            part="snippet",
            channelId=channelID,
            order="date",
            maxResults=10
        )
        response = request.execute()

        datas = []
        for x in range(10):
            a = []
            vidId = response["items"][x]["id"]["videoId"]
            vidTitle = response["items"][x]["snippet"]["title"]
            vidPic = response["items"][x]["snippet"]["thumbnails"]["high"]["url"]

            temp = response["items"][x]["snippet"]["publishedAt"]
            vidDate = ('%.10s' % temp)

            a.append(vidId)
            a.append(vidTitle)
            a.append(vidPic)
            a.append(vidDate)

            datas.append(a)

        # [('vidId','vidTitle','vidPic','vidDate'),('vidId','vidTitle','vidPic','vidDate')]
        return datas

    # API Statistics

    def statistics(channelID):

        # me       AIzaSyBcS6kuesLl9bin3DZMaTV0zUwaWWQbVxY
        # rmuti    AIzaSyAae50fLK2RJv8DDJg93SX08H0uEPCiuuU

        api_key = "AIzaSyAae50fLK2RJv8DDJg93SX08H0uEPCiuuU"
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.videos().list(
            part="statistics",
            id=channelID,
        )

        response = request.execute()

        viewCount = response["items"][0]["statistics"]["viewCount"]
        likeCount = response["items"][0]["statistics"]["likeCount"]
        dislikeCount = response["items"][0]["statistics"]["dislikeCount"]
        # commentCount = response["items"][0]["statistics"]["commentCount"]

        return [viewCount, likeCount, dislikeCount]
