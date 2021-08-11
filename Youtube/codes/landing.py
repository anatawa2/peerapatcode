from flask import Blueprint
from flask import render_template

from flask.views import View

class LandingView(View):

    def dispatch_request(self):
        print('Hello world')
        return render_template('/landing.html')