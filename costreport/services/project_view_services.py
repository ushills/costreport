from sqlalchemy.sql import func
from costreport.app import db
from costreport.data.projects import Project
from costreport.data.transactions import Transaction


def get_project_details(project_code):
    project_details = Project.query.filter(Project.project_code == project_code).first()
    return project_details


def get_project_financial_summary(project_code):
    # get total forecast_cost for project
    forecast_cost = get_forecast_cost(project_code)
    return {
        "forecast_income": 2636636,
        "forecast_cost": forecast_cost,
        "forecast_profit": 324231,
        "forecast_profit_percentage": 0.085,
    }


def get_forecast_cost(project_code):
    forecast_cost = (
        Transaction.query.with_entities(
            func.coalesce(func.sum(Transaction.value), 0).label("forecast_cost")
        )
        .join(Project, Project.id == Transaction.project_id)
        .filter(Project.project_code == project_code)
        .scalar()
    )
    return forecast_cost
