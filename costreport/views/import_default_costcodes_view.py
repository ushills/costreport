import pdb
import pathlib
import json
import os
import csv
from costreport.app import app

import flask
from flask import request
from flask_wtf import FlaskForm
from wtforms import SubmitField
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


class ImportDefaultCostcodesForm(FlaskForm):
    # Need to work around FileRequired not working with validate_on_submit
    # consider splitting into 2 forms
    csvfile = FileField(
        validators=[FileRequired(), FileAllowed(["csv"], "csv files only!")]
    )
    upload_button = SubmitField()
    save_button = SubmitField()


@blueprint.route("/upload_costcodes", methods=["GET"])
def upload_default_costcodes_get():
    form = ImportDefaultCostcodesForm(CombinedMultiDict((request.files, request.form)))
    return flask.render_template("admin/upload_default_costcodes.html", form=form)


@blueprint.route("/upload_costcodes", methods=["POST"])
def upload_default_costcodes_post():
    form = ImportDefaultCostcodesForm(CombinedMultiDict((request.files, request.form)))
    if form.validate_on_submit():
        if form.upload_button.data:
            csv_file = form.csvfile.data
            costcodes = admin_services.read_costcodes_from_csv(csv_file)
            print("upload button pressed")
            return flask.render_template(
                "admin/upload_default_costcodes.html", form=form, costcodes=costcodes
            )
        elif form.save_button.data:
            print("save button pressed")
            # TODO process to commit to the database
            return flask.redirect(flask.url_for("projects.projects"))
        else:
            print("no button pressed")

    return flask.render_template("admin/upload_default_costcodes.html", form=form)

