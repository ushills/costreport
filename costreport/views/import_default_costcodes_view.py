import json
import flask
from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from werkzeug.datastructures import CombinedMultiDict
from wtforms import HiddenField, SubmitField
from wtforms.validators import DataRequired

import costreport.services.admin_services as admin_services
from costreport.app import app

blueprint = flask.Blueprint(
    "import_default_costcodes",
    __name__,
    template_folder="templates",
    url_prefix="/admin",
)


class UploadDefaultCostcodesForm(FlaskForm):
    # Need to work around FileRequired not working with validate_on_submit
    # consider splitting into 2 forms
    csvfile = FileField(
        validators=[FileRequired(), FileAllowed(["csv"], "csv files only!")]
    )
    upload_button = SubmitField()


class SaveDefaultCostcodesForm(FlaskForm):
    save_button = SubmitField()
    costcodeData = HiddenField(validators=[DataRequired()])


@blueprint.route("/upload_costcodes", methods=["GET"])
def upload_default_costcodes_get():
    upload_form = UploadDefaultCostcodesForm(
        CombinedMultiDict((request.files, request.form))
    )
    return flask.render_template(
        "admin/upload_default_costcodes.html", upload_form=upload_form
    )


@blueprint.route("/upload_costcodes", methods=["POST"])
def upload_default_costcodes_post():
    upload_form = UploadDefaultCostcodesForm(
        CombinedMultiDict((request.files, request.form))
    )
    save_form = SaveDefaultCostcodesForm()
    if upload_form.upload_button.data and upload_form.validate():
        csv_file = upload_form.csvfile.data
        costcodes = admin_services.read_costcodes_from_csv(csv_file)
        costcodes_json = json.dumps(costcodes)
        return flask.render_template(
            "admin/upload_default_costcodes.html",
            upload_form=upload_form,
            save_form=save_form,
            costcodes=costcodes,
            costcodes_json=costcodes_json,
        )
    elif save_form.save_button.data and save_form.validate():
        costcodes_json = save_form.costcodeData.data
        costcodes = json.loads(costcodes_json)
        admin_services.save_default_costcodes_from_csvdata(costcodes)
        return flask.redirect(flask.url_for("projects.projects"))

    return flask.render_template(
        "admin/upload_default_costcodes.html",
        upload_form=upload_form,
        save_form=save_form,
    )
