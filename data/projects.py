import datetime
import os
import sys

from costreport.app import db

# Make it run more easily outside of VSCode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    created_date: datetime.datetime = db.Column(
        db.DateTime, default=datetime.datetime.now, index=True
    )
    project_code: str = db.Column(db.String, unique=True, nullable=False)
    project_name: str = db.Column(db.String, nullable=False)
    project_category: str = db.Column(db.String)
    # project_active = db.Column(db.Boolean)
