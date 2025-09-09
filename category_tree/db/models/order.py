from sqlalchemy import Column, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import INTEGER, ENUM
from sqlalchemy.orm import relationship

from .base import BaseTable


class Order(BaseTable):
    __tablename__ = "order"

    client_id = Column(
        "client_id",
        ForeignKey("client.id", ondelete="SET NULL"),
        nullable=True,
    )
    status = Column(
        "status",
        ENUM(
            "forming",
            "paid",
            "delivering",
            "done",
            "cancelled",
            name="order_status_enum",
        ),
        server_default="forming",
        nullable=False,
    )

    client = relationship("Client", back_populates="orders")
    items = relationship("OrderItem", backref="order")

class OrderItem(BaseTable):
    __tablename__ = "order_item"

    order_id = Column(
        "order_id",
        ForeignKey("order.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id = Column(
        "product_id",
        ForeignKey("product.id", ondelete="CASCADE"),
        nullable=False,
    )
    amount = Column(
        "amount",
        INTEGER,
        server_default="1",
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint('amount > 0', name='positive_amount'),
    )
