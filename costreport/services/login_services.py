from werkzeug.security import generate_password_hash, check_password_hash

from costreport.app import db
from costreport.data.users import User


def check_user_credentials(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None or not check_password(user.password, password):
        return False
    else:
        return True


def get_password_hash(password):
    return generate_password_hash(password)


def check_password(password_hash, password):
    return check_password_hash(password_hash, password)


def register_user(user_data):
    password_hash = get_password_hash(user_data["password"])
    u = User()
    u.username = user_data["username"]
    u.password = password_hash
    u.user_email = user_data["email"]
    u.active = True
    db.session.add(u)
    db.session.commit()

