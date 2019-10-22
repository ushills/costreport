from costreport.app import db
from costreport.data.projects import Project
from costreport.data.costcodes import Costcodes
from costreport.data.transactions import Transaction

# TRANSACTION FUNCTIONS
def insert_transaction(data):
    t = Transaction()
    # get the correct costcode
    costcode = (
        Costcodes.query.filter(Project.id == Costcodes.project_id)
        .filter(Project.project_code == data["project_code"])
        .filter(Costcodes.costcode == data["costcode"])
        .first()
    )
    print("Costcode.id=", costcode.id, "Project_id=", costcode.project_id)
    t.cost_code_id = costcode.id
    t.project_id = costcode.project_id
    t.value = data["value"]
    t.note = data["note"]
    db.session.add(t)
    db.session.commit()


def list_transactions():
    pass