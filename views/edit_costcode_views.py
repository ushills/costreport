import flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from costreport.services.admin_services import (
    # edit_costcode,
    check_if_costcode_exists,
    check_if_project_exists,
    get_costcodes,
)


blueprint = flask.Blueprint("edit_costcode", __name__, template_folder="templates")


class CreateCostcodeForm(FlaskForm):
    costcode = StringField("Costcode Reference", validators=[DataRequired()])
    costcode_description = StringField(
        "Costcode Description", validators=[DataRequired()]
    )
    costcode_category = StringField("Costcode category")


@blueprint.route("/admin/edit_costcode", methods=["GET"])
def edit_costcode_get():
    project = flask.request.args.get("project")
    print("GET Method")
    # check if project exists
    if check_if_project_exists(project) is False:
        flask.abort(404)
    form = CreateCostcodeForm()
    # get list of costcode data
    current_costcodes = get_costcodes(project)
    return flask.render_template(
        "admin/edit_costcode.html",
        form=form,
        project=project,
        current_costcodes=current_costcodes,
    )


@blueprint.route("/admin/edit_costcode", methods=["POST"])
def edit_costcode_post():
    project = flask.request.args.get("project")
    # get list of costcode data
    current_costcodes = get_costcodes(project)
    form = CreateCostcodeForm()
    data = {
        "project_code": project,
        "costcode": form.costcode.data,
        "costcode_description": form.costcode_description.data,
        "costcode_category": form.costcode_category.data,
    }
    if form.validate_on_submit():
        # check if the costcode already exists for the project_code
        if check_if_costcode_exists(data):
            flask.flash(
                "Costcode " + form.costcode.data + " already exists", "alert-danger"
            )
            return flask.redirect(
                flask.url_for("edit_costcode.edit_costcode_get", project=project)
            )
        # commit the data to the database
        else:
            edit_costcode(data)
            flask.flash("Costcode " + form.costcode.data + " created", "alert-success")
            return flask.redirect(
                flask.url_for("edit_costcode.edit_costcode_get", project=project)
            )
    return flask.render_template(
        "admin/edit_costcode.html",
        form=form,
        project=project,
        current_costcodes=current_costcodes,
    )