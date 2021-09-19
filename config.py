import os 
from datetime import timedelta   

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

class Config:
    DEBUG = True

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(BASE_DIR, 'dbnaja.db')
    SQLALCHEMY_DATABASE_URI = 'mysql://root:''@localhost/flaskdb'

    # pp.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flaskcodeloop'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    SECRET_KEY = 'superman'
    PERMANENT_SESSION_LIFETIME = timedelta(days=90) 
 


