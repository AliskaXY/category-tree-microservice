from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import relationship

from .base import BaseTable


class Client(BaseTable):
    __tablename__ = "client"

    name = Column(
        "name",
        TEXT,
        nullable=False,
        unique=True,
        doc="Client name.",
    )
    address = Column(
        "address",
        TEXT,
        nullable=True,
        doc="Client address.",
    )
    email = Column(
        "email",
        TEXT,
        nullable=True,
        doc="Email for notifications.",
    )

    orders = relationship("Order", back_populates="client")
