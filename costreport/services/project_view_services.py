from costreport.data.projects import Project


def get_project_details(project_code):
    project_details = Project.query.filter(Project.project_code == project_code).first()
    return project_details
