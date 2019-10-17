import os
import sys
import tempfile

import pytest

container_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, container_folder)

import costreport.app
from costreport.app import app as flask_app


@pytest.fixture
def client():
    # create temporary database for testing
    flask_app.config["TESTING"] = True
    db_temp, flask_app.config["SQLALCHEMY_DATABASE_URI"] = tempfile.mkstemp
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    client = flask_app.test_client()

    try:
        costreport.app.register_blueprints()
    except Exception as x:
        # print x
        pass

    costreport.app.setup_db()

    yield client

    # delete database when testing complete
    os.close(db_temp)
    os.unlink(flask_app.config["SQLALCHEMY_DATABASE_URI"])

