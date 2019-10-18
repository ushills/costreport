import os
import sys

import pytest

container_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, container_folder)

import costreport.app
from costreport.app import app as flask_app
from tests.client import client

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


def test_get_costcode_data(client):
    costcode_data = admin_services.get_costcode_data(
        project_code="12345", costcode="C1000"
    )
    assert costcode_data[0].costcode_description == "Costcode A"
    assert costcode_data[0].costcode_category == "Category A"


def test_check_if_costcode_exists(client):
    assert (
        admin_services.check_if_costcode_exists(project_code="12345", costcode="C1000")
        is True
    )


def test_check_if_project_does_not_exist(client):
    assert (
        admin_services.check_if_costcode_exists(project_code="76543", costcode="C1000")
        is False
    )


def test_check_if_costcode_does_not_exist(client):
    assert (
        admin_services.check_if_costcode_exists(
            project_code="12345", costcode="not exist"
        )
        is False
    )
