import datetime
import os
import sys


# Make it run more easily outside of VSCode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from costreport.app import db
from costreport.data.projects import Project


class Transaction(db.Model):
    __tablename__ = "transactions"

    id: int = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    created_date: datetime.datetime = db.Column(
        db.DateTime, default=datetime.datetime.now, index=True
    )
    project_id: str = db.Column(
        db.Integer, db.ForeignKey("projects.id"), nullable=False, index=True
    )
    cost_code_id: int = db.Column(
        db.Integer, db.ForeignKey("costcodes.id"), nullable=False, index=True
    )
    value = db.Column(db.Numeric(asdecimal=True), nullable=False)
    note: str = db.Column(db.String)
