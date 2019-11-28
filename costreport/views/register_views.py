import flask
import flask_login
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

blueprint = flask.Blueprint("register", __name__, template_folder="templates")


class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = StringField(
        "email", validators=[Email(message="Enter a valid email address")],
    )
    password = PasswordField("password", validators=[DataRequired()])
    password_confirm = PasswordField(
        "confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords do not match"),
        ],
    )


@blueprint.route("/register", methods=["GET"])
def register_get():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for("project.projects"))
    form = RegisterForm()
    return flask.render_template("user/register.html", form=form)


@blueprint.route("/register", methods=["POST"])
def register_post():
    form = RegisterForm()
    if form.validate_on_submit():
        print("run register_user function")
        user_data = {
            "username": form.username.data,
            "email": form.email.data,
            "password_hash": form.password.data,
        }
        print(user_data)
        # login_user(user)
        flask.flash("Registered")

        next = flask.request.args.get("next")
        # if not flask_login.is_safe_url(next):
        #     return flask.abort(400)

        return flask.redirect(next or flask.url_for("projects.projects"))
    return flask.render_template("user/register.html", form=form)
