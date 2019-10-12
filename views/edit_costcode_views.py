import flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from costreport.services.admin_services import (
    # edit_costcode,
    check_if_costcode_exists,
    check_if_project_exists,
    get_costcodes,
    get_costcode_data,
)


blueprint = flask.Blueprint(
    "edit_costcode", __name__, template_folder="templates", url_prefix="/admin"
)


class CreateCostcodeForm(FlaskForm):
    costcode = StringField("Costcode Reference", validators=[DataRequired()])
    costcode_description = StringField(
        "Costcode Description", validators=[DataRequired()]
    )
    costcode_category = StringField("Costcode category")


@blueprint.route("/edit_costcode", methods=["GET"])
def edit_costcode_get():
    project_code = flask.request.args.get("project")
    costcode = flask.request.args.get("costcode")
    # check if project exists
    if check_if_project_exists(project_code) is False:
        flask.abort(404)
    # check if costcode exists
    if check_if_costcode_exists(project_code=project_code, costcode=costcode) is False:
        flask.abort(404)
    form = CreateCostcodeForm()
    # get costcode data
    costcode_data = get_costcode_data(project_code=project_code, costcode=costcode)
    return flask.render_template(
        "admin/edit_costcode.html",
        form=form,
        project=project_code,
        costcode=costcode,
        costcode_data=costcode_data,
    )


@blueprint.route("/edit_costcode", methods=["POST"])
def edit_costcode_post():
    project_code = flask.request.args.get("project")
    costcode = flask.request.args.get("costcode")
    # get costcode data
    form = CreateCostcodeForm()
    data = {
        "project_code": project_code,
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
                flask.url_for("edit_costcode.edit_costcode_get", project=project_code)
            )
        # commit the data to the database
        else:
            edit_costcode(data)
            flask.flash("Costcode " + form.costcode.data + " created", "alert-success")
            return flask.redirect(
                flask.url_for("edit_costcode.edit_costcode_get", project=project_code)
            )
    return flask.render_template(
        "admin/edit_costcode.html",
        form=form,
        project=project_code,
        costcodes=costcode,
        costcode_data=costcode_data,
    )
