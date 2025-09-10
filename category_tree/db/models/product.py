from sqlalchemy import CheckConstraint, Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import INTEGER, TEXT
from sqlalchemy.orm import relationship

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

    categories = relationship("ProductCategory", back_populates="product", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("price >= 0", name="positive_price"),
        CheckConstraint("amount >= 0", name="non_negative_amount"),
    )


class ProductCategory(BaseTable):
    __tablename__ = "product_category"

    product_id = Column(
        "product_id", ForeignKey("product.id", ondelete="CASCADE"), primary_key=True, nullable=False, index=True
    )
    category_id = Column(
        "category_id", ForeignKey("category.id", ondelete="CASCADE"), primary_key=True, nullable=False, index=True
    )

    product = relationship("Product", back_populates="categories")
    category = relationship("Category", back_populates="products")

    __table_args__ = (UniqueConstraint("product_id", "category_id", name="unique_product_category"),)
