import datetime
from app import db


print("From costcodes.py, db= ", db)


class Costcodes(db.Model):
    __tablename__ = "costcodes"

    costcode_id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date: datetime.datetime = db.Column(
        db.DateTime, default=datetime.datetime.now, index=True
    )
    project_id: str = db.Column(
        db.String, db.ForeignKey("projects.project_id"), nullable=False, index=True
    )
    costcode: str = db.Column(db.String, nullable=False)
    costcode_category = db.Column(db.String, nullable=True)
    costcode_description: str = db.Column(db.String, nullable=False)
