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
import costreport.services.transaction_services as transaction_services


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

    def test_insert_a_transaction(self):
        data = {
            "project_code": "12345",
            "costcode": "C1000",
            "value": 9999,
            "note": "first transaction",
        }
        transaction_services.insert_transaction(data)

    def test_insert_2nd_transaction(self):
        data = {
            "project_code": "12345",
            "costcode": "C2000",
            "value": 1000,
            "note": "first transaction",
        }
        transaction_services.insert_transaction(data)

    def test_list_transactions(self):
        project_code = "12345"
        costcode = "C2000"
        transactions = transaction_services.list_transactions(project_code, costcode)
        assert len(transactions) == 1
        assert transactions[0].value == 1000
        assert transactions[0].note == "first transaction"
