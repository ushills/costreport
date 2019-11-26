import flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import costreport.services.admin_services as admin_services
import costreport.services.costcode_services as costcode_services
import costreport.services.projects_service as projects_service


blueprint = flask.Blueprint(
    "create_costcode", __name__, template_folder="templates", url_prefix="/admin"
)


class CreateCostcodeForm(FlaskForm):
    costcode = StringField("Costcode Reference", validators=[DataRequired()])
    costcode_description = StringField(
        "Costcode Description", validators=[DataRequired()]
    )
    costcode_category = StringField("Costcode category")


@blueprint.route("/create_costcode", methods=["GET"])
def create_costcode_get():
    project_code = flask.request.args.get("project")
    # check if project exists
    if projects_service.check_if_project_exists(project_code) is False:
        flask.abort(404)
    form = CreateCostcodeForm()
    # get list of costcode data
    current_costcodes = costcode_services.get_costcodes(project_code)
    return flask.render_template(
        "admin/create_costcode.html",
        form=form,
        project_code=project_code,
        current_costcodes=current_costcodes,
    )


@blueprint.route("/create_costcode", methods=["POST"])
def create_costcode_post():
    project = flask.request.args.get("project")
    # get list of costcode data
    current_costcodes = costcode_services.get_costcodes(project)
    form = CreateCostcodeForm()
    data = {
        "project_code": project,
        "costcode": form.costcode.data,
        "costcode_description": form.costcode_description.data,
        "costcode_category": form.costcode_category.data,
    }
    if form.validate_on_submit():
        # check if the costcode already exists for the project_code
        if costcode_services.check_if_costcode_exists(
            project_code=project, costcode=form.costcode.data
        ):
            flask.flash(
                "Costcode " + form.costcode.data + " already exists", "alert-danger"
            )
        else:
            # commit the data to the database
            admin_services.create_costcode(data)
            flask.flash("Costcode " + form.costcode.data + " created", "alert-success")
            return flask.redirect(
                flask.url_for("create_costcode.create_costcode_get", project=project)
            )
    return flask.render_template(
        "admin/create_costcode.html",
        form=form,
        project=project,
        current_costcodes=current_costcodes,
    )
