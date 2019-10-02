import datetime
from typing import List

import sqlalchemy as sa
import sqlalchemy.orm as orm
from costreport.data.modelbase import SqlAlchemyBase


class Transaction(SqlAlchemyBase):
    __tablename__ = "transactions"

    id = sa.Column(sa.Integer, primary_key=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    project_id = sa.Column(
        sa.Integer, ForeignKey("projects.project_id"), nullable=False, index=True
    )
    cost_code_id = sa.Column(
        sa.Integer, ForeignKey("costcodes.costcode_id", nullable=False, index=True)
    )
    value = sa.Column(sa.Decimal(9, 2), nullable=False)
    note = sa.Column(sa.String)
