import pathlib
import csv
from costreport.app import db
from costreport.data.projects import Project
from costreport.data.costcodes import Costcode
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


def insert_default_costcodes_from_csvdata(project_code, csvdata):
    project_id = Project.query.filter(Project.project_code == project_code).first().id
    # read the csvdata and commit to the database
    for data in csvdata:
        c = Costcode()
        c.project_id = project_id
        c.costcode = data[0]
        c.costcode_category = data[1]
        c.costcode_description = data[2]
        db.session.add(c)
    db.session.commit()
    return True


def read_costcodes_from_csv(csvfilename):
    csvfile = pathlib.Path(csvfilename)
    csvdata = []
    # read the csv file and commit to the database
    with open(csvfile, newline="") as csvfile:
        default_costcodes = csv.DictReader(csvfile, delimiter=",", quotechar='"')
        for row in default_costcodes:
            # check if costcode already exists in csvdata
            if not any(row["costcode"].strip() in data for data in csvdata):
                csvdata.append(
                    [
                        row["costcode"].strip(),
                        row["costcode_category"].strip(),
                        row["costcode_description"].strip(),
                    ]
                )
    # sort the csvdata by costcode
    csvdata.sort()
    return csvdata

