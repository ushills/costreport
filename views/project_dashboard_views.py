import flask

import costreport.services.dashboard_service as dashboard_service

blueprint = flask.Blueprint("project_dashboard", __name__, template_folder="templates")


@blueprint.route("/dashboard/<project>")
def forecast(project):
    return flask.render_template(
        "project_dashboard/project_dashboard.html", project=project
    )
