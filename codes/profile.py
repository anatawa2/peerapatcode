from flask import render_template, request, flash, session, url_for, redirect
from views import Conn
from flask.views import View
from googleapiclient.discovery import build


class MyProfile(View):
    def dispatch_request(self):
        if 'loggedin' in session:
            profile = Conn.toProfile(session['id'])
            session['role'] = profile.role

            return render_template('/profile.html', data=profile)

        return render_template('/login.html')


class UpdateProfile(View):
    def dispatch_request(self):
        if request.method == "POST":
            a = request.form['id']
            b = request.form['fullname']
            c = request.form['desc']
            d = request.form['phone']
            e = request.form['password']
            updated = Conn.toUpdate(a, b, c, d, e)
            flash('Updated')
        return redirect(url_for('profile', data=updated))


class SearchProfile(View):
    def dispatch_request(self):
        return render_template('search.html')


class SearchByTag(View):
    def dispatch_request(self):
        return render_template('tag.html')


class visit(View):
    def dispatch_request(self):
        return render_template('visit.html')


    def fetchID(channelID):
        api_key = "AIzaSyChexdcc_Ucu8qQUlFZyXDbhfiiCIFfS-A"
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.channels().list(
            part = "statistics,snippet",
            id = channelID 
        )
        response = request.execute()

        # FETCH API
        titleChannel = response["items"][0]["snippet"]["localized"]["title"]
        subscriberCount = response["items"][0]["statistics"]["subscriberCount"]
        viewCount = response["items"][0]["statistics"]["viewCount"]
        videoCount = response["items"][0]["statistics"]["videoCount"]
        publishedAt = response["items"][0]["snippet"]["publishedAt"]
        lang = response["items"][0]["snippet"]["country"]
        pic = response["items"][0]["snippet"]["thumbnails"]["high"]["url"]

        return render_template('visit.html', titleChannel=titleChannel,
                               subscriberCount=subscriberCount,
                               viewCount=viewCount,
                               videoCount=videoCount,
                               publishedAt=publishedAt,
                               lang=lang, pic=pic,)
        
