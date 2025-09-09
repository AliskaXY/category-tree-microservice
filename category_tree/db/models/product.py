from sqlalchemy import Column, CheckConstraint
from sqlalchemy.dialects.postgresql import TEXT, INTEGER

from .base import BaseTable


class Product(BaseTable):
    __tablename__ = "product"

    name = Column(
        "name",
        TEXT,
        nullable=False,
    )
    price = Column(
        "price",
        INTEGER,
        nullable=False,
    )
    amount = Column(
        "amount",
        INTEGER,
        server_default="0",
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint('price >= 0', name='check_positive_price'),
        CheckConstraint('amount >= 0', name='check_non_negative_amount'),
    )
