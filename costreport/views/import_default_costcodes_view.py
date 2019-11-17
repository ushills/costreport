import pdb
import pathlib
import json
import os
import csv
from costreport.app import app

import flask
from flask import request
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from wtforms import StringField
from wtforms.validators import DataRequired
import costreport.services.admin_services as admin_services

from costreport.services.projects_service import check_if_project_exists


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


class CostcodeDataForm(FlaskForm):
    costcodeData = HiddenField()


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
    costcodedata_form = CostcodeDataForm()
    if upload_form.upload_button.data:
        csv_file = upload_form.csvfile.data
        costcodes = admin_services.read_costcodes_from_csv(csv_file)
        costcodes_json = json.dumps(costcodes)
        return flask.render_template(
            "admin/upload_default_costcodes.html",
            upload_form=upload_form,
            save_form=save_form,
            costcodedata_form=costcodedata_form,
            costcodes=costcodes,
            costcodes_json=costcodes_json
        )
    elif save_form.save_button.data:
        print("save button pressed")
        costcodes_json = costcodedata_form.costcodeData.data
        costcodes = json.loads(costcodes_json)
        print(costcodes)
        admin_services.save_default_costcodes_from_csvdata(costcodes)
        return flask.redirect(flask.url_for("projects.projects"))
    else:
        print("no button pressed")

    return flask.render_template(
        "admin/upload_default_costcodes.html",
        upload_form=upload_form,
        save_form=save_form,
    )
