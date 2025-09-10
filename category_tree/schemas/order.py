from datetime import datetime
from enum import Enum

from pydantic import UUID4, BaseModel, field_validator
from pydantic_settings import SettingsConfigDict


class OrderStatusEnum(str, Enum):
    FORMING = "forming"
    PAID = "paid"
    DELIVERING = "delivering"
    DONE = "done"
    CANCELLED = "cancelled"


class AddOrderItemRequest(BaseModel):
    order_id: UUID4 | None = None
    client_id: UUID4 | None = None
    product_id: UUID4
    amount: int

    @field_validator("amount")
    def amount_must_be_positive(cls, v):  # pylint: disable=no-self-argument
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

    model_config = SettingsConfigDict(
        from_attributes=True,
    )


class Order(BaseModel):
    id: UUID4
    client_id: UUID4 | None
    status: OrderStatusEnum
    created_at: datetime
    updated_at: datetime
    items: list[OrderItem]

    model_config = SettingsConfigDict(
        from_attributes=True,
    )
