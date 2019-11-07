from sqlalchemy.sql import func

from costreport.data.costcodes import Costcode
from costreport.data.projects import Project
from costreport.data.transactions import Transaction


def check_if_costcode_exists(project_code, costcode):
    if (
        Costcode.query.join(Project)
        .filter(Project.project_code == project_code)
        .filter(Costcode.costcode == costcode)
        .first()
    ):
        return True
    return False


def get_costcodes(project_code):
    costcodes = (
        Costcode.query.join(Project)
        .filter(Project.project_code == project_code)
        .order_by(Costcode.costcode.asc())
        .all()
    )
    return costcodes


def get_costcode_data(project_code, costcode):
    costcode_data = (
        Costcode.query.join(Project)
        .filter(Project.project_code == project_code)
        .filter(Costcode.costcode == costcode)
        .one()
    )
    return costcode_data


def get_costcodes_and_transaction_values(project_code):
    costcodes_and_values = (
        Costcode.query.with_entities(
            Project.project_code,
            Costcode.costcode,
            Costcode.costcode_description,
            func.coalesce(func.sum(Transaction.value), 0).label("transaction_sum"),
        )
        .join(Project, Project.id == Costcode.project_id)
        .outerjoin(Transaction, Transaction.costcode_id == Costcode.id)
        .filter(Project.project_code == project_code)
        .group_by(Costcode.costcode)
        .all()
    )
    return costcodes_and_values
