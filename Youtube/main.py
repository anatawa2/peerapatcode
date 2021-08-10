from app import app, db
import views
from codes.profile import profile 
from codes.auth import users

app.register_blueprint(profile, url_prefix='/profile')
app.register_blueprint(users, url_prefix='/')

db.create_all()


if __name__ == '__main__':
    app.run()
