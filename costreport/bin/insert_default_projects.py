import os
import sys
import pathlib
import csv

# Make it run more easily outside of VSCode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from costreport.app import db
from costreport.data.projects import Project


def main():
    while True:
        insert_default_projects()


def insert_default_projects():
    csvfilename = pathlib.Path("infrastruture/projects_default.csv")

    with open(csvfilename, newline="") as csvfile:
        default_projects = csv.DictReader(csvfile, delimiter=",", quotechar='"')
        for row in default_projects:
            p = Project()
            p.project_id = row["project_id"]
            p.project_name = row["project_name"]

            db.session.add(p)
    db.session.commit()
    print("Committed to database")


if __name__ == "__main__":
    main()
