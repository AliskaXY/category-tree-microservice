from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr
from pydantic_settings import SettingsConfigDict


class Client(BaseModel):
    id: UUID4
    name: str
    email: EmailStr | None = None
    address: str | None = None
    dt_created: datetime
    dt_updated: datetime

    model_config = SettingsConfigDict(
        from_attributes = True,
    )


class ClientCreateRequest(BaseModel):
    name: str
    email: EmailStr | None = None
    address: str | None = None

    model_config = SettingsConfigDict(
        extra = "forbid",
    )


class ClientTotal(BaseModel):
    name: str
    total: int
