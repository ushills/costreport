import flask
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from costreport.services.transaction_services import (
    insert_transaction,
    get_current_transactions,
)
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
    costcode_data = get_costcode_data(project, costcode)
    transactions, transactions_sum = get_current_transactions(project, costcode)
    return flask.render_template(
        "transaction/insert_transaction.html",
        form=form,
        project=project,
        costcode=costcode,
        costcode_data=costcode_data,
        transactions=transactions,
        transactions_sum=transactions_sum,
    )


@blueprint.route("/insert_transaction", methods=["POST"])
def insert_transaction_post():
    project = flask.request.args.get("project")
    costcode = flask.request.args.get("costcode")
    costcode_data = get_costcode_data(project, costcode)
    transactions, transactions_sum = get_current_transactions(project, costcode)
    form = InsertTransactionForm()
    data = {
        "project_code": project,
        "costcode": costcode,
        "transaction_value": form.transaction_value.data,
        "transaction_note": form.transaction_note.data,
    }
    if form.validate_on_submit():
        # TODO check that the value string can be converted to a number
        try:
            float(form.transaction_value.data)
        except ValueError:
            flask.flash("Value must be a number", "alert-danger")
        else:
            # commit the data to the database
            insert_transaction(data)
            flask.flash("Transaction created", "alert-success")
            return flask.redirect(
                flask.url_for(
                    "insert_transaction.insert_transaction_get",
                    project=project,
                    costcode_data=costcode_data,
                )
            )
    return flask.render_template(
        "transaction/insert_transaction.html",
        form=form,
        project=project,
        costcode=costcode,
        costcode_data=costcode_data,
        transactions=transactions,
        transactions_sum=transactions_sum,
    )
