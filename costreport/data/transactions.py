import datetime
import os
import sys

from costreport.app import db

# Make it run more easily outside of VSCode
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


class Transaction(db.Model):
    __tablename__ = "transactions"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date: datetime.datetime = db.Column(
        db.DateTime, default=datetime.datetime.now, index=True
    )
    project_id: int = db.Column(
        db.Integer, db.ForeignKey("projects.id"), nullable=False, index=True
    )
    costcode_id: int = db.Column(
        db.Integer, db.ForeignKey("costcodes.id"), nullable=False, index=True
    )
    value = db.Column(db.Numeric(asdecimal=True), nullable=False)
    note: str = db.Column(db.String)
    project = db.relationship("Project", uselist=False)
    costcode = db.relationship("Costcode", back_populates="transactions", uselist=False)
