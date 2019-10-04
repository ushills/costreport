import flask
import os
import sys

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)

import costreport.data.db_session as db_session

app = flask.Flask(__name__)


def main():
    register_blueprints()
    setup_db()
    app.run(host="0.0.0.0", debug=True)
    # app.run(debug=True)


def setup_db():
    db_file = os.path.join(os.path.dirname(__file__), "db", "costreport.sqlite")
    db_session.global_init(db_file)


def register_blueprints():
    from costreport.views import projects_views
    from costreport.views import project_forecast_views
    from costreport.views import project_dashboard_views
    from costreport.views import project_costdetail_views

    app.register_blueprint(projects_views.blueprint)
    app.register_blueprint(project_forecast_views.blueprint)
    app.register_blueprint(project_dashboard_views.blueprint)
    app.register_blueprint(project_costdetail_views.blueprint)


if __name__ == "__main__":
    main()
