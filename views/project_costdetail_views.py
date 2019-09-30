import flask

import costreport.services.costdetail_service as costdetail_service

blueprint = flask.Blueprint("project_costdetail", __name__, template_folder="templates")


@blueprint.route("/<project>/costdetail/<cost_code>")
def costdetail(project, cost_code):
    cost_detail = costdetail_service.get_cost_detail(project, cost_code)
    return flask.render_template(
        "cost_detail/costdetail.html",
        project=project,
        cost_code=cost_code,
        cost_detail=cost_detail,
    )
