import flask
from flask_wtf import FlaskForm
from flask_wtf import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField
from wtforms.validators import DataRequired
from costreport.services.admin_services import (
    read_costcodes_from_csv,
    insert_default_costcodes_from_csvdata,
)
from costreport.services.projects_service import check_if_project_exists


blueprint = flask.Blueprint(
    "import_default_costcodes",
    __name__,
    template_folder="templates",
    url_prefix="/admin",
)


class ImportDefaultCostcodesForm(FlaskForm):
    csvfile = FileField(validators=[FileRequired()], FileAllowed(["csv"], "csv files only!"))


@blueprint.route("/upload_costcodes", methods=["GET", "POST"])
def upload_default_costcodes():
    project = flask.request.args.get("project")
    # check if project exists
    if check_if_project_exists(project) is False:
        flask.abort(404)
    form = ImportDefaultCostcodesForm()
    if form.validate_on_submit():
        f = form.csvfile.data
        csvfilename = secure_filename(f.filename)
        csvdata = admin_services.read_costcodes_from_csv(csvfilename)
        return redirect(
            flask.url_for("import_default_costcodes_view.view_costcodes", project=project, csvdata=csvdata)
        )
    return flask.render_template(
        "admin/upload_costcodes",
        form=form,
        project=project,        
    )


@blueprint.route("/view_uploaded_costcodes", methods=["GET", "POST"])
def view_default_costcodes():
    # check if csvdata exists
    if csvdata is None:
        flask.abort(404)
    return flask.render_template(
        "admin/view_uploaded_costcodes",
        csvdata = csvdata
    )
    
