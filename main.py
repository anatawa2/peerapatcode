from views import *
from codes.profile import *
from codes.auth import *
from codes.messages import *


# Register/Login
app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/register', view_func=RoleRegister.as_view('register'))
app.add_url_rule('/register/<role>', view_func=RoleRegister.pick_role)
app.add_url_rule(
    '/registered', view_func=RoleRegister.submit_role, methods=["POST"])
app.add_url_rule(
    '/login', view_func=LoginForm.as_view('login'), methods=["POST"])
app.add_url_rule('/logout', view_func=LoginForm.logout)

# Profile
app.add_url_rule('/profile/', view_func=MyProfile.as_view('profile'))
app.add_url_rule('/profile/update',
                 view_func=UpdateProfile.as_view('update'), methods=["POST"])
app.add_url_rule('/profile/upload',
                 view_func=UpdateProfile.uploadIMG, methods=["POST"])
app.add_url_rule('/profile/upload2', view_func=UpdateProfile.uploadIMG2)
app.add_url_rule(
    '/profile/tag', view_func=SaveTag.as_view('tagged'), methods=["POST"])

# Search
app.add_url_rule('/search', view_func=SearchProfile.searchName)
app.add_url_rule('/search/profile',
                 view_func=SearchProfile.as_view('search'), methods=["POST"])
app.add_url_rule('/search/tag', view_func=SearchByTag.as_view('tag'))
app.add_url_rule('/search/tag/<tag>', view_func=SearchByTag.getTag)
app.add_url_rule('/Recommended', view_func=Recommended.as_view('recommended'))
app.add_url_rule('/visit/<id>', view_func=Visit.VisitTo)

# Messagess
app.add_url_rule('/inbox', view_func=Chatting.as_view('inboxes'))
app.add_url_rule('/messages/<sendto>', view_func=Chatting.inbox,)
app.add_url_rule('/messages/send',
                 view_func=Chatting.message, methods=["POST"])


db.create_all()
 
 

if __name__ == '__main__':
    app.run()
