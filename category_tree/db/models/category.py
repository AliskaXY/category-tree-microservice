from sqlalchemy import Column, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import relationship

from .base import BaseTable


class Category(BaseTable):
    __tablename__ = "category"

    name = Column(
        "name",
        TEXT,
        nullable=False,
    )
    parent_id = Column(
        "parent_id",
        ForeignKey("category.id", ondelete="CASCADE"),
        nullable=True,
    )
    root_id = Column(
        "root_id",
        ForeignKey("category.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    parent = relationship(
        "Category", 
        remote_side="Category.id", 
        backref="children",
        foreign_keys=[parent_id]
    )  
    root = relationship(
        "Category", 
        remote_side="Category.id",
        foreign_keys=[root_id]
    )

    __table_args__ = (
        CheckConstraint(
            '''
            (parent_id IS NULL AND root_id IS NULL) OR 
            (parent_id IS NOT NULL AND root_id IS NOT NULL)
            ''',
            name='check_parent_root_consistency'
        ),
    )