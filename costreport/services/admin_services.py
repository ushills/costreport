import pathlib
import csv
from costreport.app import db
from costreport.data.projects import Project
from costreport.data.costcodes import Costcode
from costreport.data.transactions import Transaction
from costreport.data.default_costcodes import DefaultCostcode


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
    # TODO increment the version of the costcodes and drop all but the last
    # read the csvdata and commit to the database
    for data in costcodes_list:
        d = DefaultCostcode()
        d.costcode = data[0]
        d.costcode_category = data[1]
        d.costcode_description = data[2]
        db.session.add(d)
    db.session.commit()
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
