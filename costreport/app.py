import os
import sys

import flask
import flask_login
from flask_sqlalchemy import SQLAlchemy

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, folder)

app = flask.Flask(__name__)
app.secret_key = "temporary secret key"  # change before production

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

db_file = "sqlite:///db/costreport.sqlite"
app.config["SECRET_KEY"] = "password"
app.config["SQLALCHEMY_DATABASE_URI"] = db_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


def main():
    register_blueprints()
    setup_db()

    # app.run(host="0.0.0.0", debug=True)
    app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)


def setup_db():
    from costreport.data.__all_models import db

    db.init_app(app)
    db.create_all()


def register_blueprints():
    from costreport.views import projects_views
    from costreport.views import project_view_views
    from costreport.views import project_costdetail_views
    from costreport.views import create_project_views
    from costreport.views import create_costcode_views
    from costreport.views import edit_costcode_views
    from costreport.views import insert_transaction_views
    from costreport.views import import_default_costcodes_view
    from costreport.views import add_default_costcodes_to_project_views
    from costreport.views import login_views
    from costreport.views import register_views

    app.register_blueprint(projects_views.blueprint)
    app.register_blueprint(project_view_views.blueprint)
    app.register_blueprint(project_costdetail_views.blueprint)
    app.register_blueprint(create_project_views.blueprint)
    app.register_blueprint(create_costcode_views.blueprint)
    app.register_blueprint(edit_costcode_views.blueprint)
    app.register_blueprint(insert_transaction_views.blueprint)
    app.register_blueprint(import_default_costcodes_view.blueprint)
    app.register_blueprint(add_default_costcodes_to_project_views.blueprint)
    app.register_blueprint(login_views.blueprint)
    app.register_blueprint(register_views.blueprint)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return flask.render_template("errors/404.html"), 404


if __name__ == "__main__":
    main()
