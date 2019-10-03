import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from costreport.data.modelbase import SqlAlchemyBase


class Project(SqlAlchemyBase):
    __tablename__ = "projects"

    project_id: str = sa.Column(sa.String, primary_key=True, nullable=False)
    created_date: datetime.datetime = sa.Column(
        sa.DateTime, default=datetime.datetime.now, index=True
    )
    project_name: str = sa.Column(sa.String, nullable=False)
    project_category: str = sa.Column(sa.String)
