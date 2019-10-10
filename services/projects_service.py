from costreport.data.projects import Project


def get_project_list():
    projects = Project.query.order_by(Project.project_code.desc()).all()
    return projects
