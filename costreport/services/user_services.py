from werkzeug.security import generate_password_hash, check_password_hash

from costreport.app import db
from costreport.data.users import User


def check_user_credentials(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(user.password):
        return False
    else:
        return True


def register_user(user_data):
    password_hash = get_password_hash(user_data["password"])
    u = User()
    u.username = user_data["username"]
    u.password = password_hash
    u.user_email = user_data["email"]
    u.active = True
    db.session.add(u)
    db.session.commit()


@login_manager.user_loader
def user_loader(username):
    users = User.query.all()
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    users = User.query.all()
    username = request.form.get("username")
    if username not in users:
        return

    user = User()
    user.username = username

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form["password"] == users[username]["password"]

    return user
