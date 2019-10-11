from costreport.app import db
from costreport.data.projects import Project
from costreport.data.costcodes import Costcodes


# CREATE PROJECT FUNCTIONS #
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


# CREATE COSTCODE FUNCTIONS #
def check_if_costcode_exists(data):
    project_code = data["project_code"]
    costcode = data["costcode"]
    if (
        Costcodes.query.filter(Project.project_code == project_code)
        .filter(Costcodes.costcode == costcode)
        .first()
    ):
        return True


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
        Costcodes.query.filter(Project.project_code == project_code)
        .order_by(Costcodes.costcode.asc())
        .all()
    )
    return costcodes
