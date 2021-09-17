from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config 
from jinja2 import Environment  
import pusher

app = Flask(__name__)
app.config.from_object(Config)  

jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])
app.jinja_env.add_extension('jinja2.ext.loopcontrols')  

pusher_client = pusher.Pusher(
            app_id='1266085',
            key='37d67f096ee63c8b35d7',
            secret='320d58bd8258c730d390',
            cluster='ap1',
            ssl=True
        )

 
db = SQLAlchemy(app)


 

