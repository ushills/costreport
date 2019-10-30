from costreport.data.projects import Project


def get_project_details(project_code):
    project_details = Project.query.filter(Project.project_code == project_code).first()
    return project_details


def get_project_financial_summary(project_code):
    return {
        "forecast_income": 2636636,
        "forecast_cost": 2343224,
        "forecast_profit": 324231,
        "forecast_profit_percentage": 0.085,
    }
