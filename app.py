import os
import sys

import flask
from flask_sqlalchemy import SQLAlchemy

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)

app = flask.Flask(__name__)

# db_file = "sqlite:///" + os.path.join(
#     os.path.dirname(__file__), "db", "costreport.sqlite"
# )

db_file = "sqlite:///db/costreport.sqlite"
app.config["SECRET_KEY"] = "password"
app.config["SQLALCHEMY_DATABASE_URI"] = db_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


def main():
    # from costreport.data.projects import db
    from costreport.data.__all_models import db

    db.init_app(app)
    db.create_all()

    register_blueprints()

    app.run(host="0.0.0.0", debug=True)
    # app.run(debug=True)


def register_blueprints():
    from costreport.views import projects_views
    from costreport.views import project_forecast_views
    from costreport.views import project_dashboard_views
    from costreport.views import project_costdetail_views
    from costreport.views import createproject_views

    app.register_blueprint(projects_views.blueprint)
    app.register_blueprint(project_forecast_views.blueprint)
    app.register_blueprint(project_dashboard_views.blueprint)
    app.register_blueprint(project_costdetail_views.blueprint)
    app.register_blueprint(createproject_views.blueprint)


if __name__ == "__main__":
    main()
