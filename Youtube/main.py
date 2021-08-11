from app import app, db
import views
from codes.profile import profile 
from codes.auth import users
from codes.landing import LandingView

app.register_blueprint(profile, url_prefix='/profile')
app.register_blueprint(users, url_prefix='/')

app.add_url_rule('/landing', view_func=LandingView.as_view('landing'))

db.create_all()


if __name__ == '__main__':
    app.run()
