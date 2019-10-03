import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from costreport.data.modelbase import SqlAlchemyBase
from costreport.data.costcode_category import CostcodeCategory


class Costcodes(SqlAlchemyBase):
    __tablename__ = "costcodes"

    costcode_id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date: datetime.datetime = sa.Column(
        sa.DateTime, default=datetime.datetime.now, index=True
    )
    project_id: str = sa.Column(
        sa.String, sa.ForeignKey("projects.project_id"), nullable=False, index=True
    )
    costcode: str = sa.Column(sa.String, nullable=False)
    costcode_category_id: int = sa.Column(
        sa.Integer, sa.ForeignKey("costcode_category.costcode_category_id")
    )
    costcode_category = orm.relationship(
        "CostcodeCategory", back_populates="costcode_category"
    )
    costcode_description: str = sa.Column(sa.String, nullable=False)
