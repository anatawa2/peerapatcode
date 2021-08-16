from app import app, db
from views import *
from codes.profile import *
from codes.auth import *
from sqlalchemy import delete


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
app.add_url_rule('/search', view_func=SearchProfile.as_view('search'))
app.add_url_rule('/tag', view_func=SearchByTag.as_view('tag'))
app.add_url_rule('/visit', view_func=visit.as_view('visit'))


db.create_all()


def adds(a):

    stmt = style.insert().values(user_id = session['id'], tag_id = a)
    db.session.execute(stmt)
    db.session.commit()

def dels(a):
    stmt = (delete(style).where( style.c.user_id == session['id'],style.c.tag_id == a))
    db.session.execute(stmt)
    db.session.commit()



if __name__ == '__main__':
    app.run()
