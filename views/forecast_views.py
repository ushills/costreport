import flask

import costreport.services.forecast_service as forecast_service

blueprint = flask.Blueprint("forecast", __name__, template_folder="templates")


@blueprint.route("/forecast")
def forecast():
    forecast_detail = forecast_service.get_forecast_detail()
    return flask.render_template(
        "forecast/forecast.html", forecast_detail=forecast_detail
    )
