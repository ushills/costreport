import os
import sys
import pathlib
import csv

# Make it run more easily outside of VSCode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import costreport.data.db_session as db_session
from costreport.data.costcodes import Costcodes


def main():
    init_db()
    while True:
        insert_default_costcodes()


def insert_default_costcodes():
    project_id = input("Project id:").strip().lower()
    if len(project_id) < 1:
        raise ValueError("Value cannot be NULL")

    csvfilename = pathlib.Path("infrastruture/costcodes_default.csv")

    session = db_session.create_session()

    with open(csvfilename, newline="") as csvfile:
        default_costcodes = csv.DictReader(csvfile, delimiter=",", quotechar='"')
        for row in default_costcodes:
            c = Costcodes()
            c.project_id = project_id
            c.costcode = row["costcode"]
            c.costcode_category = row["costcode_category"]
            c.costcode_description = row["costcode_description"]

            session.add(c)
    session.commit()
    print("Committed to database")


# def insert_a_costcode():
#     c = Costcodes()
#     c.project_id = input("Project id:").strip().lower()
#     if len(c.project_id) < 1:
#         raise ValueError("Value cannot be NULL")
#     c.costcode = input("Costcode ref:").strip().lower()
#     if len(c.costcode) < 1:
#         raise ValueError("Value cannot be NULL")
#     c.cost_code_description = input("Costcode Description:").strip()
#     if len(c.cost_code_description) < 1:
#         raise ValueError("Value cannot be NULL")

#     session = db_session.create_session()
#     session.add(c)
#     session.commit()


def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join("..", "db", "costreport.sqlite")
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)


if __name__ == "__main__":
    main()
