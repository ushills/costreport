import os
import sys
import pytest

container_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, container_folder)

import costreport.app
from costreport.app import app as flask_app


@pytest.fixture(scope="module")
def client():
    # create temporary database for testing
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    client = flask_app.test_client()

    from costreport.data.__all_models import db

    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()
