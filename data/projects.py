import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from costreport.data.modelbase import SqlAlchemyBase


class Project(SqlAlchemyBase):
    __tablename__ = "projects"

    project_id = sa.Column(sa.String, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    project_name = sa.Column(sa.String, nullable=False)
