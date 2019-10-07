from costreport.data.projects import Project


def get_project_list():
    projects = Project.query.all()
    # print(projects)
    return projects
