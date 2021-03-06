import csv
from sqlalchemy.sql import exists

from costreport.app import db
from costreport.data.costcodes import Costcode
from costreport.data.default_costcodes import DefaultCostcode
from costreport.data.projects import Project


# PROJECT ADMIN FUNCTIONS #
def create_project(data):
    p = Project()
    p.project_code = data["project_code"]
    p.project_name = data["project_name"]
    db.session.add(p)
    db.session.commit()


# COSTCODE ADMIN FUNCTIONS #
def create_costcode(data):
    c = Costcode()
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
        Costcode.query.filter(Project.id == Costcode.project_id)
        .filter(Project.project_code == data["project_code"])
        .filter(Costcode.costcode == data["costcode"])
        .first()
    )
    # update the category or description
    costcode.costcode_category = data["costcode_category"]
    costcode.costcode_description = data["costcode_description"]
    db.session.commit()


def save_default_costcodes_from_csvdata(costcodes_list):
    # read the csvdata and commit to the database
    for data in costcodes_list:
        d = DefaultCostcode()
        d.costcode = data[0]
        d.costcode_category = data[1]
        d.costcode_description = data[2]
        d.active = False
        db.session.add(d)
    db.session.commit()
    # delete the currently active default costcodes
    old_costcodes = DefaultCostcode.query.filter(
        DefaultCostcode.active == True
    ).delete()
    # db.session.commit()
    print(old_costcodes, "costcodes deleted")
    # make the new cost default costcodes active
    new_costcodes = DefaultCostcode.query.filter(
        DefaultCostcode.active == False
    ).update({DefaultCostcode.active: True}, synchronize_session=False)
    db.session.commit()
    print(new_costcodes, "costcodes added")
    return True


def read_costcodes_from_csv(csv_file):
    csv_file_data = csv_file.read()
    # decode csv_file_data binary to string
    csv_file_data = csv_file_data.decode()
    # create list of dictionaries keyed by header row
    default_costcodes = [
        {k: v for k, v in row.items()}
        for row in csv.DictReader(csv_file_data.splitlines(), skipinitialspace=True)
    ]
    # process the default_costcodes to omit the header row if present
    costcodes = []
    for row in default_costcodes:
        if not any(row["costcode"].strip() in data for data in costcodes):
            costcodes.append(
                [
                    row["costcode"].strip(),
                    row["costcode_category"].strip(),
                    row["costcode_description"].strip(),
                ]
            )
    # sort the csvdata by costcode
    costcodes.sort()
    return costcodes


def add_default_costcodes_to_project(project_code):
    # get the active default_costcodes from the database
    default_costcodes = (
        DefaultCostcode.query.filter(DefaultCostcode.active == True)
        .order_by(DefaultCostcode.costcode)
        .all()
    )
    print(default_costcodes[0])
    # add the default costcodes to the project
    project_id = Project.query.filter(Project.project_code == project_code).first().id
    for default_costcode in default_costcodes:
        c = Costcode()
        c.project_id = project_id
        c.costcode = default_costcode.costcode
        c.costcode_description = default_costcode.costcode_description
        c.costcode_category = default_costcode.costcode_category
        db.session.add(c)
    db.session.commit()
    return True


def check_if_project_has_costcodes(project_code):
    costcodes_exists = (
        Costcode.query.join(Project, Project.id == Costcode.project_id)
        .filter(Project.project_code == project_code)
        .first()
    ) is not None
    return costcodes_exists

