import flask

import costreport.services.forecast_service as forecast_service
import costreport.services.transaction_services as transaction_services

blueprint = flask.Blueprint("project_forecast", __name__, template_folder="templates")


@blueprint.route("/<project>/forecast")
def forecast(project):
    # forecast_detail = forecast_service.get_forecast_detail()
    forecast_detail = transaction_services.get_costcodes_and_transaction_sum(project)
    forecast_summary = forecast_service.get_summary_detail()
    return flask.render_template(
        "forecast/forecast.html",
        project=project,
        forecast_detail=forecast_detail,
        forecast_summary=forecast_summary,
    )
