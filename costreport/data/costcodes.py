import datetime
import os
import sys

# Make it run more easily outside of VSCode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from costreport.app import db
from costreport.data.projects import Project


class Costcodes(db.Model):
    __tablename__ = "costcodes"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date: datetime.datetime = db.Column(
        db.DateTime, default=datetime.datetime.now, index=True
    )
    project_id: int = db.Column(
        db.Integer, db.ForeignKey("projects.id"), nullable=False, index=True
    )
    costcode: str = db.Column(db.String, nullable=False)
    costcode_category: str = db.Column(db.String, nullable=True)
    costcode_description: str = db.Column(db.String, nullable=False)
