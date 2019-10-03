import sqlalchemy as sa

# import sqlalchemy.orm as orm
from costreport.data.modelbase import SqlAlchemyBase


class CostcodeCategories(SqlAlchemyBase):
    __tablename__ = "costcode_category"

    costcode_category_id: int = sa.Column(
        sa.Integer, primary_key=True, autoincrement=True
    )
    costcode_category: str = sa.Column(sa.String)
