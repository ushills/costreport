import flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import costreport.services.admin_services as admin_services
import costreport.services.costcode_services as costcode_services
import costreport.services.project_view_services as project_view_services
import costreport.services.projects_service as projects_service


blueprint = flask.Blueprint(
    "edit_costcode", __name__, template_folder="templates", url_prefix="/admin"
)


class CreateCostcodeForm(FlaskForm):
    # costcode = StringField("Costcode Reference", validators=[DataRequired()])
    costcode_description = StringField("Description", validators=[DataRequired()])
    costcode_category = StringField("Category")


@blueprint.route("/edit_costcode", methods=["GET"])
def edit_costcode_get():
    project_code = flask.request.args.get("project")
    costcode = flask.request.args.get("costcode")
    # check if project exists
    if projects_service.check_if_project_exists(project_code) is False:
        flask.abort(404)
    # check if costcode exists
    if (
        costcode_services.check_if_costcode_exists(
            project_code=project_code, costcode=costcode
        )
        is False
    ):
        flask.abort(404)
    # get project details
    project_details = project_view_services.get_project_details(project_code)
    form = CreateCostcodeForm()
    # get costcode data
    costcode_data = costcode_services.get_costcode_data(
        project_code=project_code, costcode=costcode
    )
    return flask.render_template(
        "admin/edit_costcode.html",
        form=form,
        project_details=project_details,
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
        "costcode": costcode,
        "costcode_description": form.costcode_description.data,
        "costcode_category": form.costcode_category.data,
    }
    if form.validate_on_submit():
        admin_services.update_costcode(data)
        flask.flash("Costcode " + costcode + " edited", "alert-success")
        return flask.redirect(
            flask.url_for(
                "edit_costcode.edit_costcode_get",
                project=project_code,
                costcode=costcode,
            )
        )
    return flask.render_template(
        "admin/edit_costcode.html", form=form, costcode_data=costcode_data,
    )
