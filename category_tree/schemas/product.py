from datetime import datetime

from pydantic import UUID4, BaseModel, field_validator
from pydantic_settings import SettingsConfigDict


class Product(BaseModel):
    id: UUID4
    name: str
    price: int
    amount: int
    dt_created: datetime
    dt_updated: datetime

    model_config = SettingsConfigDict(
        from_attributes=True,
    )


class ProductCreateRequest(BaseModel):
    name: str
    price: int
    amount: int

    @field_validator("price")
    def price_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Price must be positive")
        return v

    @field_validator("amount")
    def amount_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Amount must be positive")
        return v


class ProductTotalSold(BaseModel):
    product_name: str
    root_category_name: str
    total_sold: int
