import datetime
import os
import sys

from costreport.app import db

# Make it run more easily outside of VSCode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


class Project(db.Model):
    __tablename__ = "projects"

    project_id: str = db.Column(db.String, primary_key=True, nullable=False)
    created_date: datetime.datetime = db.Column(
        db.DateTime, default=datetime.datetime.now, index=True
    )
    project_name: str = db.Column(db.String, nullable=False)
    project_category: str = db.Column(db.String)
