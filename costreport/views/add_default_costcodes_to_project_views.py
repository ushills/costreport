import flask
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms.validators import DataRequired
from costreport.services.admin_services import create_costcode
from costreport.services.costcode_services import (
    check_if_costcode_exists,
    get_costcodes,
)
from costreport.services.projects_service import check_if_project_exists

blueprint = flask.Blueprint(
    "add_default_costcodes_to_project",
    __name__,
    template_folder="templates",
    url_prefix="/admin",
)


class AddDefaultCostcodesForm(FlaskForm):
    tick_box = BooleanField("Apply default costcodes", validators=[DataRequired()])


@blueprint.route("/add_default_costcodes_to_project", methods=["GET"])
def add_default_costcodes_to_project_get():
    project = flask.request.args.get("project")
    # check if the project exists
    if check_if_project_exists(project) is False:
        flask.abort(404)
    form = AddDefaultCostcodesForm()
    # check if there are existing costcodes
    if len(get_costcodes(project)) > 0:
        flask.flash("Costcodes already exist, defaults cannot be imported")
        costcodes_exists = True
    else:
        costcodes_exists = False
    return flask.render_template(
        "admin/add_default_costcodes_to_project.html",
        form=form,
        project=project,
        costcodes_exists=costcodes_exists,
    )

@blueprint.route("/add_default_costcodes_to_project", methods=["POST"])
def add_default_costcodes_to_project_post():
    project = flask.request.args.get("project")
    
