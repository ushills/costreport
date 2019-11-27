import flask
import flask_login
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

blueprint = flask.Blueprint("login", __name__, template_folder="templates")


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


@blueprint.route("/login", methods=["GET"])
def login_get():
    if flask_login.current_user.is_authenticated:
        return redirect(flask.url_for("project.projects"))
    form = LoginForm()
    return flask.render_template("login/login.html", form=form)


@blueprint.route("/login", methods=["POST"])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        print("run login_user function")
        # login_user(user)
        flask.flash("Logged in")

        next = flask.request.args.get("next")
        # if not flask_login.is_safe_url(next):
        #     return flask.abort(400)

        return flask.redirect(next or flask.url_for("projects.projects"))
    return flask.render_template("login/login.html", form=form)
