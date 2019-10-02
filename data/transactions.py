import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from costreport.data.modelbase import SqlAlchemyBase


class Transaction(SqlAlchemyBase):
    __tablename__ = "transactions"

    id: int = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    created_date: datetime.datetime = sa.Column(
        sa.DateTime, default=datetime.datetime.now, index=True
    )
    project_id: int = sa.Column(
        sa.Integer, sa.ForeignKey("projects.project_id"), nullable=False, index=True
    )
    cost_code_id: int = sa.Column(
        sa.Integer, sa.ForeignKey("costcodes.costcode_id", nullable=False, index=True)
    )
    value = sa.Column(sa.Numeric(asdecimal=True), nullable=False)
    note: str = sa.Column(sa.String)
