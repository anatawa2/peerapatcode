from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from jinja2 import Environment


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'superman' 
jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])

db = SQLAlchemy(app)


