from costreport.data.projects import Project


def check_if_project_exists(project_code):
    if Project.query.filter(Project.project_code == project_code).first():
        return True
    return False


def get_project_list():
    projects = Project.query.order_by(Project.project_code.desc()).all()
    return projects
