import flask
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from costreport.services.admin_services import create_project, check_if_project_exists


blueprint = flask.Blueprint("createproject", __name__, template_folder="templates")


class CreateProjectForm(FlaskForm):
    project_code = StringField("Project Reference", validators=[DataRequired()])
    project_name = StringField("Project Name", validators=[DataRequired()])


@blueprint.route("/admin/createproject", methods=["GET"])
def createproject_get():
    form = CreateProjectForm()
    return flask.render_template("admin/createproject.html", form=form)


@blueprint.route("/admin/createproject", methods=["POST"])
def createproject_post():
    form = CreateProjectForm()
    data = {
        "project_code": form.project_code.data,
        "project_name": form.project_name.data,
    }
    if form.validate_on_submit():
        # check if the project code already exists
        if check_if_project_exists(data):
            flask.redirect("admin/createproject.html")
        # commit the data to the database
        else:
            create_project(data)
            return flask.redirect("createproject/success")
    return flask.render_template("admin/createproject.html", form=form)


@blueprint.route("/admin/createproject/success")
def formcreated():
    return "Form Created"
