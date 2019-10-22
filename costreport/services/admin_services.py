from costreport.app import db
from costreport.data.projects import Project
from costreport.data.costcodes import Costcodes
from costreport.data.transactions import Transaction


# PROJECT FUNCTIONS #
def check_if_project_exists(project_code):
    if Project.query.filter(Project.project_code == project_code).first():
        return True
    return False


def create_project(data):
    p = Project()
    p.project_code = data["project_code"]
    p.project_name = data["project_name"]
    db.session.add(p)
    db.session.commit()


# COSTCODE FUNCTIONS #
def check_if_costcode_exists(project_code, costcode):
    if (
        Costcodes.query.filter(Project.id == Costcodes.project_id)
        .filter(Project.project_code == project_code)
        .filter(Costcodes.costcode == costcode)
        .first()
    ):
        return True
    return False


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


def get_costcodes(project_code):
    costcodes = (
        Costcodes.query.filter(Project.id == Costcodes.project_id)
        .filter(Project.project_code == project_code)
        .order_by(Costcodes.costcode.asc())
        .all()
    )
    return costcodes


def get_costcode_data(project_code, costcode):
    costcode_data = (
        Costcodes.query.filter(Project.id == Costcodes.project_id)
        .filter(Project.project_code == project_code)
        .filter(Costcodes.costcode == costcode)
        .first()
    )
    return costcode_data


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
