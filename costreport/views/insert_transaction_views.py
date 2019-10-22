import flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from costreport.services.transaction_services import insert_transaction
from costreport.services.projects_service import check_if_project_exists
from costreport.services.costcode_services import (
    check_if_costcode_exists,
    get_costcode_data,
)

blueprint = flask.Blueprint("insert_transaction", __name__, template_folder="templates")


class InsertTransactionForm(FlaskForm):
    transaction_value = StringField("Value", validators=[DataRequired()])
    transaction_note = StringField("Note", validators=[DataRequired()])


@blueprint.route("/insert_transaction", methods=["GET"])
def insert_transaction_get():
    project = flask.request.args.get("project")
    costcode = flask.request.args.get("costcode")
    # check if project exists
    if check_if_project_exists(project) is False:
        flask.abort(404)
    # check if costcode exists
    if check_if_costcode_exists(project, costcode) is False:
        flask.abort(404)
    form = InsertTransactionForm()
    # TODO add list of transactions for costcode
    costcode = get_costcode_data(project, costcode)
    return flask.render_template(
        "transaction/insert_transaction.html",
        form=form,
        project=project,
        costcode=costcode,
    )


# TODO
# @blueprint.route("/create_costcode", methods=["POST"])
# def create_costcode_post():
#     project = flask.request.args.get("project")
#     # get list of costcode data
#     current_costcodes = get_costcodes(project)
#     form = CreateCostcodeForm()
#     data = {
#         "project_code": project,
#         "costcode": form.costcode.data,
#         "costcode_description": form.costcode_description.data,
#         "costcode_category": form.costcode_category.data,
#     }
#     if form.validate_on_submit():
#         # check if the costcode already exists for the project_code
#         if check_if_costcode_exists(project_code=project, costcode=form.costcode.data):
#             flask.flash(
#                 "Costcode " + form.costcode.data + " already exists", "alert-danger"
#             )
#         else:
#             # commit the data to the database
#             create_costcode(data)
#             flask.flash("Costcode " + form.costcode.data + " created", "alert-success")
#             return flask.redirect(
#                 flask.url_for("create_costcode.create_costcode_get", project=project)
#             )
#     return flask.render_template(
#         "admin/create_costcode.html",
#         form=form,
#         project=project,
#         current_costcodes=current_costcodes,
#     )
