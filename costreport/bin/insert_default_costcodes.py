import os
import sys
import pathlib
import csv

# Make it run more easily outside of VSCode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from costreport.app import db
from costreport.data.costcodes import Costcode


def main():
    while True:
        insert_default_costcodes()


def insert_default_costcodes():
    project_id = input("Project id:").strip().lower()
    if len(project_id) < 1:
        raise ValueError("Value cannot be NULL")

    csvfilename = pathlib.Path("infrastruture/costcodes_default.csv")

    with open(csvfilename, newline="") as csvfile:
        default_costcodes = csv.DictReader(csvfile, delimiter=",", quotechar='"')
        for row in default_costcodes:
            c = Costcode()
            c.project_id = project_id
            c.costcode = row["costcode"]
            c.costcode_category = row["costcode_category"]
            c.costcode_description = row["costcode_description"]

            db.session.add(c)
    db.session.commit()
    print("Committed to database")


if __name__ == "__main__":
    main()
