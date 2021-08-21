import os 

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(BASE_DIR, 'dbnaja.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 


