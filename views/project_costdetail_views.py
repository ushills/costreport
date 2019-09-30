import flask
from flask import request

import costreport.services.costdetail_service as costdetail_service

blueprint = flask.Blueprint("project_costdetail", __name__, template_folder="templates")


@blueprint.route("/<project>/costdetail")
def costdetail(project):
    cost_code = request.args.get("cost_code")
    cost_detail = costdetail_service.get_cost_detail(project, cost_code)
    cost_summary = costdetail_service.get_cost_summary(project, cost_code)
    print(cost_summary)
    return flask.render_template(
        "cost_detail/costdetail.html",
        project=project,
        cost_code=cost_code,
        cost_detail=cost_detail,
        cost_summary=cost_summary,
    )
