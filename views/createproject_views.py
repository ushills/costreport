import flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


blueprint = flask.Blueprint("createproject", __name__, template_folder="templates")


class CreateProjectForm(FlaskForm):
    project_number = StringField("project_number", validators=[DataRequired()])
    project_name = StringField("project_name", validators=[DataRequired()])


@blueprint.route("/admin/createproject", methods=["POST", "GET"])
def createproject():
    form = CreateProjectForm()
    print(form.project_number.data, form.project_name.data)
    return flask.render_template("admin/createproject.html", form=form)

