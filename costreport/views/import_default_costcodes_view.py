import pdb
import pathlib
import json
import os
from costreport.app import app

import flask
from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from wtforms import StringField
from wtforms.validators import DataRequired
import costreport.services.admin_services as admin_services

from costreport.services.projects_service import check_if_project_exists


blueprint = flask.Blueprint(
    "import_default_costcodes", __name__, template_folder="templates", url_prefix="/admin"
)


class ImportDefaultCostcodesForm(FlaskForm):
    csvfile = FileField(
        validators=[FileRequired(), FileAllowed(["csv"], "csv files only!")]
    )


@blueprint.route("/upload_costcodes", methods=["GET", "POST"])
def upload_default_costcodes():
    form = ImportDefaultCostcodesForm(CombinedMultiDict((request.files, request.form)))
    if form.validate_on_submit():
        f = form.csvfile.data
        filename = secure_filename(f.filename)
        filepath = os.path.join(app.instance_path, "csv_uploads", filename)
        f.save(filepath)
        try:
            csvdata = admin_services.read_costcodes_from_csv(filepath)
            costcodes = json.dumps(csvdata)
            # breakpoint()
            # os.remove(filepath)
            return res
        except:
            os.remove(filepath)
        return flask.redirect(
            flask.url_for(
                "import_default_costcodes.view_default_costcodes", costcodes=costcodes
            )
        )
    return flask.render_template("admin/upload_default_costcodes.html", form=form)


@blueprint.route("/view_uploaded_costcodes", methods=["GET", "POST"])
def view_default_costcodes():
    costcodes = flask.request.args.get("costcodes")
    costcodes = json.loads(costcodes)

    if costcodes is None:
        flask.abort(404)

    return flask.render_template(
        "admin/view_uploaded_costcodes.html", costcodes=costcodes
    )
