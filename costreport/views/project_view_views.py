import flask

import costreport.services.project_view_services as project_view_services
import costreport.services.transaction_services as transaction_services
import costreport.services.costcode_services as costcode_services

blueprint = flask.Blueprint("project_view", __name__, template_folder="templates")


@blueprint.route("/<project>")
def project_view(project):
    project_details = project_view_services.get_project_details(project)
    project_costcode_detail = transaction_services.get_costcodes_and_transaction_sum(
        project
    )
    project_financial_summary = project_view_services.get_project_financial_summary(
        project
    )
    return flask.render_template(
        "project/project.html",
        project_details=project_details,
        project_costcode_detail=project_costcode_detail,
        project_financial_summary=project_financial_summary,
    )


@blueprint.route("/<project>/costcodes")
def costcodes_view(project):
    project_details = project_view_services.get_project_details(project)
    project_costcode_detail = costcode_services.get_costcodes(project)
    project_financial_summary = project_view_services.get_project_financial_summary(
        project
    )
    return flask.render_template(
        "project/costcode.html",
        project_details=project_details,
        project_costcode_detail=project_costcode_detail,
        project_financial_summary=project_financial_summary,
    )
