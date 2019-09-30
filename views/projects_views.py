import flask

import costreport.services.projects_service as projects_service

blueprint = flask.Blueprint("projects", __name__, template_folder="templates")


@blueprint.route("/projects")
def projects():
    project_list = projects_service.get_project_list()
    return flask.render_template("projects/projects.html", projects=project_list)
