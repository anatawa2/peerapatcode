from flask import Flask
from  flask_sqlalchemy import  SQLAlchemy
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'superman'
db = SQLAlchemy(app)


