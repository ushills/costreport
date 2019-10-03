from typing import List
import sqlalchemy.orm

import costreport.data.db_session as db_session
from costreport.data.projects import Project


def get_project_list() -> List:
    session = db_session.create_session()

    projects = session.query(Project).order_by(Project.project_id.desc()).all()
    print(type(projects))
    session.close()

    return projects
