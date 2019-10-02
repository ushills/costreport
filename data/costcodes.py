import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from costreport.data.modelbase import SqlAlchemyBase


class Costcodes(SqlAlchemyBase):
    __tablename__ = "costcodes"

    costcode_id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date: datetime.datetime = sa.Column(
        sa.DateTime, default=datetime.datetime.now, index=True
    )
    project_id: int = sa.Column(
        sa.Integer, sa.ForeignKey("projects.project_id"), nullable=False, index=True
    )
    costcode: str = sa.Column(sa.String, nullable=False)
    cost_code_description: str = sa.Column(sa.String, nullable=False)

