import flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


blueprint = flask.Blueprint("createproject", __name__, template_folder="templates")


class CreateProjectForm(FlaskForm):
    project_reference = StringField(validators=[DataRequired()])
    project_name = StringField(validators=[DataRequired()])
    submit = SubmitField()


@blueprint.route("/admin/createproject", methods=["GET"])
def createproject_get():
    form = CreateProjectForm()
    print(form.project_reference.data, form.project_name.data)
    return flask.render_template("admin/createproject.html", form=form)


@blueprint.route("/admin/createproject", methods=["POST"])
def createproject_post():
    form = CreateProjectForm()
    print(form.project_reference.data, form.project_name.data)
    return flask.render_template("admin/createproject.html", form=form)
