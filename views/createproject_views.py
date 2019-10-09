import flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


blueprint = flask.Blueprint("createproject", __name__, template_folder="templates")


class CreateProjectForm:
    project_reference = StringField(validators=[DataRequired()])
    project_name = StringField(validators=[DataRequired()])


@blueprint.route("/admin/createproject", methods=["GET"])
def createproject_get():
    return flask.render_template("admin/createproject.html")


@blueprint.route("/admin/createproject", methods=["POST"])
def createproject_post():
    request = flask.request
    project_reference = request.project_reference
    project_name = request.project_name
    print(project_reference)
    print(project_name)
    return flask.render_template("admin/createproject.html", form=form)
