import datetime
from app import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id: int = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    created_date: datetime.datetime = db.Column(
        db.DateTime, default=datetime.datetime.now, index=True
    )
    project_id: str = db.Column(
        db.Integer, db.ForeignKey("projects.project_id"), nullable=False, index=True
    )
    cost_code_id: int = db.Column(
        db.Integer, db.ForeignKey("costcodes.costcode_id"), nullable=False, index=True
    )
    value = db.Column(db.Numeric(asdecimal=True), nullable=False)
    note: str = db.Column(db.String)
