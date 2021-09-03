import os
from flask import render_template, request, flash, session, url_for, redirect
from views import *
from flask.views import View
from werkzeug.utils import secure_filename
from googleapiclient.discovery import build
import random


def vdo():
    api_key = "AIzaSyAae50fLK2RJv8DDJg93SX08H0uEPCiuuU"
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        channelId="UCUfnk5CgUjykoc-BezLMMIA",
        maxResults=1
    )
    response = request.execute()
    vidId = response["items"][0]["id"]["videoId"]
    vidTitle = response["items"][0]["snippet"]["title"]
    vidPic = response["items"][0]["snippet"]["thumbnails"]["high"]

    return [vidId, vidTitle, vidPic]


a = vdo()
print(a)