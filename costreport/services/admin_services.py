from costreport.app import db
from costreport.data.projects import Project
from costreport.data.costcodes import Costcodes
from costreport.data.transactions import Transaction


# PROJECT ADMIN FUNCTIONS #
def create_project(data):
    p = Project()
    p.project_code = data["project_code"]
    p.project_name = data["project_name"]
    db.session.add(p)
    db.session.commit()


# COSTCODE ADMIN FUNCTIONS #
def create_costcode(data):
    c = Costcodes()
    project_code = data["project_code"]
    project = Project.query.filter(Project.project_code == project_code).first()
    c.project_id = project.id
    c.costcode = data["costcode"]
    c.costcode_description = data["costcode_description"]
    c.costcode_category = data["costcode_category"]
    db.session.add(c)
    db.session.commit()


def update_costcode(data):
    # get the costcode
    costcode = (
        Costcodes.query.filter(Project.id == Costcodes.project_id)
        .filter(Project.project_code == data["project_code"])
        .filter(Costcodes.costcode == data["costcode"])
        .first()
    )
    # update the category or description
    costcode.costcode_category = data["costcode_category"]
    costcode.costcode_description = data["costcode_description"]
    db.session.commit()
