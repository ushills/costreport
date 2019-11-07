import os
import sys

# Make it run more easily outside of VSCode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import costreport.data.db_session as db_session
from costreport.data.costcodes import Costcode


def main():
    init_db()
    while True:
        insert_a_costcode()


def insert_a_costcode():
    c = Costcode()
    c.project_id = input("Project id:").strip().lower()
    if len(c.project_id) < 1:
        raise ValueError("Value cannot be NULL")
    c.costcode = input("Costcode ref:").strip().lower()
    if len(c.costcode) < 1:
        raise ValueError("Value cannot be NULL")
    c.cost_code_description = input("Costcode Description:").strip()
    if len(c.cost_code_description) < 1:
        raise ValueError("Value cannot be NULL")

    session = db_session.create_session()
    session.add(c)
    session.commit()


def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join("..", "db", "costreport.sqlite")
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)


if __name__ == "__main__":
    main()
