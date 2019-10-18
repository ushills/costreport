import os
import sys

import pytest

container_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, container_folder)

import costreport.app
from costreport.app import app as flask_app
from tests.client import client

import costreport.services.admin_services as admin_services
import costreport.services.projects_service as projects_service


class TestProjectServices:
    def test_add_projects_to_database(self, client):
        project_list = [
            {"project_code": "12345", "project_name": "Project A"},
            {"project_code": "54321", "project_name": "Project B"},
            {"project_code": "15423", "project_name": "Project C"},
            {"project_code": "65432", "project_name": "Project D"},
        ]

        for project in project_list:
            admin_services.create_project(project)

    def test_retrieve_projects_from_database_in_order(self):

        db_project_list = projects_service.get_project_list()

        assert db_project_list[0].project_code == "65432"
        assert db_project_list[1].project_code == "54321"
        assert db_project_list[2].project_code == "15423"
        assert db_project_list[3].project_code == "12345"

    def test_project_exists(self):
        assert admin_services.check_if_project_exists("12345") is True

    def test_project_does_not_exist(self):
        assert admin_services.check_if_project_exists("76543") is False
