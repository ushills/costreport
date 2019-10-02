import os
import sys

# Make it run more easily outside of VSCode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import costreport.data.db_session as db_session
from costreport.data.projects import Project
from costreport.data.costcodes import Costcodes


def main():
    init_db()
    while True:
        print("enter data")
        insert_a_project()


def insert_a_project():
    p = Project()
    p.project_id = input("Project id:").strip().lower()
    p.project_name = input("Project name:").strip()

    session = db_session.create_session()
    session.add(p)
    session.commit()


def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join("..", "db", "costreport.sqlite")
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)


if __name__ == "__main__":
    main()
