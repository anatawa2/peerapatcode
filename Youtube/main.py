from app import app, db
import views
from codes.profile import *
from codes.auth import *
from codes.landing import LandingView


app.add_url_rule('/landing', view_func=LandingView.as_view('landing'))

# Register/Login
app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/register', view_func=RoleRegister.as_view('register'))
app.add_url_rule('/register/<role>', view_func=RoleRegister.pick_role)
app.add_url_rule('/registered', view_func=RoleRegister.submit_role,methods = ["POST"])
app.add_url_rule('/login', view_func=LoginForm.as_view('login'),methods = ["POST"])
app.add_url_rule('/logout', view_func=LoginForm.logout)

# Profile
app.add_url_rule('/profile/', view_func=MyProfile.as_view('profile'))
app.add_url_rule('/profile/update', view_func=UpdateProfile.as_view('update'),methods = ["POST"])
app.add_url_rule('/search', view_func=SearchProfile.as_view('search'))
app.add_url_rule('/tag', view_func=SearchByTag.as_view('tag'))



db.create_all()

if __name__ == '__main__':
    app.run()
