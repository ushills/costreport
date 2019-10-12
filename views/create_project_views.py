import flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from costreport.services.admin_services import create_project, check_if_project_exists


blueprint = flask.Blueprint("create_project", __name__, template_folder="templates")


class CreateProjectForm(FlaskForm):
    project_code = StringField("Project Reference", validators=[DataRequired()])
    project_name = StringField("Project Name", validators=[DataRequired()])


@blueprint.route("/admin/create_project", methods=["GET"])
def create_project_get():
    form = CreateProjectForm()
    return flask.render_template("admin/create_project.html", form=form)


@blueprint.route("/admin/create_project", methods=["POST"])
def create_project_post():
    form = CreateProjectForm()
    data = {
        "project_code": form.project_code.data,
        "project_name": form.project_name.data,
    }
    if form.validate_on_submit():
        # check if the project code already exists
        if check_if_project_exists(form.project_code.data):
            flask.flash(
                "Project " + form.project_code.data + " already exists", "alert-danger"
            )
            return flask.redirect(flask.url_for("create_project.create_project_get"))
        # commit the data to the database
        else:
            create_project(data)
            flask.flash("Project " + form.project_code.data + " created", "alert-success")
            return flask.redirect(flask.url_for("create_project.create_project_get"))
    return flask.render_template("admin/create_project.html", form=form)
