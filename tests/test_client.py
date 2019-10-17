import os
import sys
import tempfile

import pytest

container_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, container_folder)

import costreport.app
from costreport.app import app as flask_app

import costreport.services.admin_services as admin_services
import costreport.services.projects_service as projects_service


@pytest.fixture
def client():
    # create temporary database for testing
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
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
    # os.close(db_temp)
    # os.unlink(db)


def test_add_project_to_database(client):
    project_list = [
        {"project_code": "12345", "project_name": "Project A"},
        {"project_code": "54321", "project_name": "Project B"},
        {"project_code": "15423", "project_name": "Project C"},
        {"project_code": "65432", "project_name": "Project D"},
    ]

    for project in project_list:
        admin_services.create_project(project)

    db_project_list = projects_service.get_project_list()

    assert db_project_list[0].project_code == "65432"
    assert db_project_list[1].project_code == "54321"
    assert db_project_list[2].project_code == "15423"
    assert db_project_list[3].project_code == "12345"

