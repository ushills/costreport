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


class TestTransactionServices:
    def test_setup_project(self, client):
        project_list = [{"project_code": "12345", "project_name": "Project A"}]

        for project in project_list:
            admin_services.create_project(project)

    def test_add_a_costcode(self):
        costcode_list = [
            {
                "project_code": "12345",
                "costcode": "C1000",
                "costcode_description": "Costcode A",
                "costcode_category": "Category A",
            },
            {
                "project_code": "12345",
                "costcode": "C2000",
                "costcode_description": "Costcode B",
                "costcode_category": "Category B",
            },
        ]
        for data in costcode_list:
            admin_services.create_costcode(data)

    def test_add_a_transaction(self):
        data = {
            "project_code": "12345",
            "costcode": "C1000",
            "value": 9999,
            "note": "first transaction",
        }
        admin_services.insert_transaction(data)

    def test_add_2nd_transaction(self):
        data = {
            "project_code": "12345",
            "costcode": "C2000",
            "value": 1000,
            "note": "first transaction",
        }
        admin_services.insert_transaction(data)
