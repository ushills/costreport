import os
import sys

import pytest

container_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, container_folder)

import costreport.app
from costreport.app import app as flask_app
from costreport.tests.client import client

import costreport.services.admin_services as admin_services


def test_add_a_project_to_database(client):
    project_list = [{"project_code": "12345", "project_name": "Project A"}]

    for project in project_list:
        admin_services.create_project(project)


def test_add_a_costcode(client):
    data = {
        "project_code": "12345",
        "costcode": "C1000",
        "costcode_description": "Costcode A",
        "costcode_category": "Category A",
    }
    admin_services.create_costcode(data)


def test_get_costcodes(client):
    assert admin_services.get_costcodes("12345")[0].costcode == "C1000"
