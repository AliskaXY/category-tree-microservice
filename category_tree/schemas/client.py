from datetime import datetime

from pydantic import BaseModel, UUID4, EmailStr

class Client(BaseModel):
    id: UUID4
    name: str
    email: EmailStr | None = None
    address: str | None = None
    dt_created: datetime
    dt_updated: datetime

    class Config:
        orm_mode = True

class ClientCreateRequest(BaseModel):
    name: str
    email: EmailStr | None = None
    address: str | None = None

    class Config:
        extra = "forbid"

class ClientTotal(BaseModel):
    name: str
    total: int
