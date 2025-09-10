from datetime import datetime
from enum import Enum

from pydantic import UUID4, BaseModel, field_validator


class OrderStatusEnum(str, Enum):
    forming = "forming"
    paid = "paid"
    delivering = "delivering"
    done = "done"
    cancelled = "cancelled"


class AddOrderItemRequest(BaseModel):
    order_id: UUID4 | None = None
    client_id: UUID4 | None = None
    product_id: UUID4
    amount: int

    @field_validator("amount")
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v


class OrderItem(BaseModel):
    id: UUID4
    order_id: UUID4
    product_id: UUID4
    amount: int
    dt_created: datetime
    dt_updated: datetime

    class Config:
        from_attributes = True


class Order(BaseModel):
    id: UUID4
    client_id: UUID4 | None
    status: OrderStatusEnum
    created_at: datetime
    updated_at: datetime
    items: list[OrderItem]

    class Config:
        from_attributes = True
