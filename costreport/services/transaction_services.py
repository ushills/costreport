from sqlalchemy.sql import func

from costreport.app import db
from costreport.data.costcodes import Costcodes
from costreport.data.projects import Project
from costreport.data.transactions import Transaction


# TRANSACTION FUNCTIONS
def insert_transaction(data):
    t = Transaction()
    # get the correct costcode
    costcode = (
        Costcodes.query.filter(Project.id == Costcodes.project_id)
        # .join(Project)
        .filter(Project.project_code == data["project_code"])
        .filter(Costcodes.costcode == data["costcode"])
        .first()
    )
    # print("Costcode.id=", costcode.id, "Project_id=", costcode.project_id)
    t.costcode_id = str(costcode.id)
    t.project_id = str(costcode.project_id)
    t.value = data["transaction_value"]
    t.note = data["transaction_note"]
    db.session.add(t)
    db.session.commit()


def get_current_transactions(project_code, costcode):
    transactions = (
        Transaction.query.filter(Project.id == Transaction.project_id)
        .filter(Costcodes.id == Transaction.costcode_id)
        .filter(Costcodes.id == Transaction.costcode_id)
        .filter(Project.project_code == project_code)
        .filter(Costcodes.costcode == costcode)
        .order_by(Transaction.created_date.desc())
    )
    transactions_sum = transactions.with_entities(db.func.sum(Transaction.value)).scalar()
    if transactions_sum is None:
        transactions_sum = 0
    transactions = transactions.all()
    return transactions, transactions_sum


def get_costcodes_and_transaction_sum(project_code):
    costcodes_transaction_sum = (
        Transaction.query.with_entities(
            Costcodes.costcode,
            Costcodes.costcode_description,
            func.sum(Transaction.value).label("forecast_cost_total"),
        )
        .filter(Transaction.costcode_id == Costcodes.id)
        .filter(Project.id == Transaction.project_id)
        .filter(Project.project_code == project_code)
        .group_by(Costcodes.costcode)
        .order_by(Costcodes.costcode)
        .all()
    )
    return costcodes_transaction_sum
