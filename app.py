import flask
import os
import sys

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)

app = flask.Flask(__name__)


def main():
    register_blueprints()
    app.run(debug=True)


def register_blueprints():
    from costreport.views import projects_views
    from costreport.views import forecast_views
    from views import forecast_views

    app.register_blueprint(projects_views.blueprint)
    app.register_blueprint(forecast_views.blueprint)


if __name__ == "__main__":
    main()
