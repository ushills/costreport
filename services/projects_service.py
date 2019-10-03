# from typing import List
import os
import sys
import sqlalchemy.orm

# # Make it run more easily outside of VSCode
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


import costreport.data.db_session as db_session
from costreport.data.projects import Project


def get_project_list():
    session = db_session.create_session()

    projects = session.query(Project).order_by(Project.project_id.desc()).all()

    session.close()

    return projects


# def init_db():
#     top_folder = os.path.dirname(__file__)
#     rel_file = os.path.join("..", "db", "costreport.sqlite")
#     db_file = os.path.abspath(os.path.join(top_folder, rel_file))
#     db_session.global_init(db_file)


# if __name__ == "__main__":
#     init_db()
#     get_project_list()
