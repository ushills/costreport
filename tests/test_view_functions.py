import os
import sys

container_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, container_folder)

from tests.client import client

import costreport.services.admin_services as admin_services
import costreport.services.projects_service as projects_service
import costreport.services.project_view_services as project_view_services
import costreport.services.costcode_services as costcode_services
import costreport.services.transaction_services as transaction_services


class TestPopulateDatabase:
    def test_add_projects(self, client):
        project_list = [
            {"project_code": "12345", "project_name": "Project A"},
            {"project_code": "54321", "project_name": "Project B"},
            {"project_code": "15423", "project_name": "Project C"},
            {"project_code": "65432", "project_name": "Project D"},
        ]

        for project in project_list:
            admin_services.create_project(project)

    def test_add_costcodes(self):
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
            {
                "project_code": "12345",
                "costcode": "C3000",
                "costcode_description": "Costcode C",
                "costcode_category": "Category C",
            },
            {
                "project_code": "54321",
                "costcode": "C3000",
                "costcode_description": "Costcode B",
                "costcode_category": "Category B",
            },
        ]
        for data in costcode_list:
            admin_services.create_costcode(data)

    def test_add_transactions(self):
        transaction_list = [
            {
                "project_code": "12345",
                "costcode": "C1000",
                "transaction_value": 9999,
                "transaction_note": "first transaction",
            },
            {
                "project_code": "12345",
                "costcode": "C2000",
                "transaction_value": 1000,
                "transaction_note": "first transaction",
            },
            {
                "project_code": "54321",
                "costcode": "C3000",
                "transaction_value": 1000,
                "transaction_note": "first transaction",
            },
        ]
        for transaction in transaction_list:
            transaction_services.insert_transaction(transaction)


class TestProjectServices:
    def test_retrieve_projects_from_database_in_order(self):

        db_project_list = projects_service.get_project_list()

        assert db_project_list[0].project_code == "65432"
        assert db_project_list[1].project_code == "54321"
        assert db_project_list[2].project_code == "15423"
        assert db_project_list[3].project_code == "12345"

    def test_project_exists(self):
        assert projects_service.check_if_project_exists("12345") is True

    def test_project_does_not_exist(self):
        assert projects_service.check_if_project_exists("76543") is False


class TestCostcodeServices:
    def test_get_all_costcodes(self):
        assert len(costcode_services.get_costcodes("12345")) == 3
        assert costcode_services.get_costcodes("12345")[0].costcode == "C1000"
        assert costcode_services.get_costcodes("12345")[1].costcode == "C2000"
        assert costcode_services.get_costcodes("12345")[1].costcode == "C2000"

    def test_get_costcode_data(self):
        costcode_data = costcode_services.get_costcode_data(
            project_code="12345", costcode="C1000"
        )
        assert costcode_data.project.project_name == "Project A"
        assert costcode_data.costcode_description == "Costcode A"
        assert costcode_data.costcode_category == "Category A"

    def test_get_costcodes_and_transaction_values(self):
        data = costcode_services.get_costcodes_and_transaction_values("12345")
        assert data == [
            ("12345", "C1000", "Costcode A", 9999),
            ("12345", "C2000", "Costcode B", 1000),
            ("12345", "C3000", "Costcode C", 0),
        ]

    def test_check_if_costcode_exists(self):
        assert (
            costcode_services.check_if_costcode_exists(
                project_code="12345", costcode="C1000"
            )
            is True
        )

    def test_check_if_project_does_not_exist(self):
        assert (
            costcode_services.check_if_costcode_exists(
                project_code="76543", costcode="C1000"
            )
            is False
        )

    def test_check_if_costcode_does_not_exist(self):
        assert (
            costcode_services.check_if_costcode_exists(
                project_code="12345", costcode="not exist"
            )
            is False
        )

    def test_admin_update_costcode(self):
        data = {
            "project_code": "12345",
            "costcode": "C1000",
            "costcode_description": "Updated description",
            "costcode_category": "Updated category",
        }
        admin_services.update_costcode(data)
        costcode_data = costcode_services.get_costcode_data(
            project_code="12345", costcode="C1000"
        )
        assert costcode_data.project.project_name == "Project A"
        assert costcode_data.costcode_description == "Updated description"
        assert costcode_data.costcode_category == "Updated category"


class TestProjectViewServices:
    def test_get_project_details(self):
        project_code = "12345"
        project_details = project_view_services.get_project_details(project_code)
        assert project_details.project_code == "12345"
        assert project_details.project_name == "Project A"
        assert project_details.project_category is None


class TestTransactionServices:
    def test_get_current_transactions(self):
        project_code = "12345"
        costcode = "C2000"
        transactions, transactions_sum = transaction_services.get_current_transactions(
            project_code, costcode
        )
        assert len(transactions) == 1
        assert transactions[0].value == 1000
        assert transactions[0].note == "first transaction"
        assert transactions[0].project.project_code == "12345"
        assert transactions[0].project.project_name == "Project A"
        assert transactions[0].costcode.costcode_description == "Costcode B"
        assert transactions_sum == 1000

    def test_get_costcodes_and_transaction_sum(self):
        project_code = "12345"
        transactions_by_costcode = transaction_services.get_costcodes_and_transaction_sum(
            project_code
        )
        assert len(transactions_by_costcode) == 2
        assert transactions_by_costcode[0].costcode == "C1000"
        assert transactions_by_costcode[1].costcode == "C2000"
        assert transactions_by_costcode[0].forecast_cost_total == 9999
        assert transactions_by_costcode[1].forecast_cost_total == 1000
