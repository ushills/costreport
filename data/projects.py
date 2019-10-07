import datetime
from app import db


print("From projects.py, db= ", db)


class Project(db.Model):
    __tablename__ = "projects"

    project_id: str = db.Column(db.String, primary_key=True, nullable=False)
    created_date: datetime.datetime = db.Column(
        db.DateTime, default=datetime.datetime.now, index=True
    )
    project_name: str = db.Column(db.String, nullable=False)
    project_category: str = db.Column(db.String)
