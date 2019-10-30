from sqlalchemy.sql import func

from costreport.data.costcodes import Costcodes
from costreport.data.projects import Project


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
