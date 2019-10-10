from costreport.app import db
from costreport.data.projects import Project


def create_project(data):
    p = Project()
    p.project_code = data["project_code"]
    p.project_name = data["project_name"]
    db.session.add(p)
    db.session.commit()
    print(data)
