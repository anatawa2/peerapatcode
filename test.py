from re import X
from flask import render_template, request, flash, session, url_for, redirect
from views import *
from flask.views import View
from googleapiclient.discovery import build

api_key = "AIzaSyChexdcc_Ucu8qQUlFZyXDbhfiiCIFfS-A"
youtube = build("youtube", "v3", developerKey=api_key)
request = youtube.channels().list(
    part="snippet,statistics",
    id="UCuTTT_6JxuAtRdvF3BvVjdg"
)
response = request.execute()

# # FETCH API
# titleChannel = response["items"][0]["snippet"]["localized"]["title"]
# subscriberCount = response["items"][0]["statistics"]["subscriberCount"]

# viewCounts = response["items"][0]["statistics"]["viewCount"]
# viewCount = format(int(response["items"][0]["statistics"]["viewCount"]),",")
# videoCount = response["items"][0]["statistics"]["videoCount"]

# publishedAt = response["items"][0]["snippet"]["publishedAt"]
# lang = response["items"][0]["snippet"]["country"]
# pic = response["items"][0]["snippet"]["thumbnails"]["high"]["url"]


print(response)
