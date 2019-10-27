from costreport.app import db
from costreport.data.projects import Project
from costreport.data.costcodes import Costcodes
from costreport.data.transactions import Transaction

# TRANSACTION FUNCTIONS
def insert_transaction(data):
    t = Transaction()
    # get the correct costcode
    costcode = (
        Costcodes.query.join(Project)
        .filter(Project.project_code == data["project_code"])
        .filter(Costcodes.costcode == data["costcode"])
        .first()
    )
    # print("Costcode.id=", costcode.id, "Project_id=", costcode.project_id)
    t.cost_code_id = costcode.id
    t.project_id = costcode.project_id
    t.value = data["transaction_value"]
    t.note = data["transaction_note"]
    db.session.add(t)
    db.session.commit()


def get_current_transactions(project_code, costcode):
    transactions = (
        Transaction.query.join(Project, Costcodes)
        .filter(Costcodes.id == Transaction.cost_code_id)
        .filter(Project.project_code == project_code)
        .filter(Costcodes.costcode == costcode)
        .order_by(Transaction.created_date.desc())
    )
    transactions_sum = transactions.with_entities(db.func.sum(Transaction.value)).scalar()
    transactions = transactions.all()
    return transactions, transactions_sum
