import flask

import costreport.services.project_view_services as project_view_services

blueprint = flask.Blueprint("project_view", __name__, template_folder="templates")


@blueprint.route("/<project>")
def project_view(project):
    project_details = project_view_services.get_project_details(project)
    return flask.render_template(
        "project_view/project_view.html", project_details=project_details
    )
