import flask
import os
import sys

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)

app = flask.Flask(__name__)


def main():
    register_blueprints()
    app.run(host="0.0.0.0", debug=True)


def register_blueprints():
    from costreport.views import projects_views
    from costreport.views import forecast_views
    from costreport.views import project_dashboard_views

    app.register_blueprint(projects_views.blueprint)
    app.register_blueprint(forecast_views.blueprint)
    app.register_blueprint(project_dashboard_views.blueprint)


if __name__ == "__main__":
    main()
