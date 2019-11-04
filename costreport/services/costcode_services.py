from sqlalchemy.sql import func

from costreport.data.costcodes import Costcodes
from costreport.data.projects import Project
from costreport.data.transactions import Transaction


def check_if_costcode_exists(project_code, costcode):
    if (
        Costcodes.query.join(Project)
        .filter(Project.project_code == project_code)
        .filter(Costcodes.costcode == costcode)
        .first()
    ):
        return True
    return False


def get_costcodes(project_code):
    costcodes = (
        Costcodes.query.join(Project)
        .filter(Project.project_code == project_code)
        .order_by(Costcodes.costcode.asc())
        .all()
    )
    return costcodes


def get_costcode_data(project_code, costcode):
    costcode_data = (
        Costcodes.query.join(Project)
        .filter(Project.project_code == project_code)
        .filter(Costcodes.costcode == costcode)
        .one()
    )
    return costcode_data


def get_costcodes_and_transaction_values(project_code):
    costcodes_and_values = (
        Costcodes.query.with_entities(
            Project.project_code,
            Costcodes.costcode,
            Costcodes.costcode_description,
            func.coalesce(func.sum(Transaction.value), 0).label("transaction_sum"),
        )
        .join(Project, Project.id == Costcodes.project_id)
        .outerjoin(Transaction, Transaction.cost_code_id == Costcodes.id)
        .filter(Project.project_code == project_code)
        .group_by(Costcodes.costcode)
        .all()
    )
    return costcodes_and_values
