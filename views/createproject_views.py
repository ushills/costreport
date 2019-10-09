import flask
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


blueprint = flask.Blueprint("createproject", __name__, template_folder="templates")


class CreateProjectForm(FlaskForm):
    project_reference = StringField(validators=[DataRequired()])
    project_name = StringField(validators=[DataRequired()])


@blueprint.route("/admin/createproject", methods=["GET"])
def createproject_get():
    form = CreateProjectForm()
    return flask.render_template("admin/createproject.html", form=form)


@blueprint.route("/admin/createproject", methods=["POST"])
def createproject_post():
    # project_reference = request.form.get("project_reference")
    # project_name = request.form.get("project_name")
    # print(project_reference, project_name)
    form = CreateProjectForm()
    print(form.project_reference.data, form.project_name.data)
    return flask.render_template("admin/createproject.html", form=form)
