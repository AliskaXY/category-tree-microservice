from datetime import datetime

from pydantic import BaseModel, UUID4

class Category(BaseModel):
    id: UUID4
    name: str
    parent_id: UUID4 | None = None
    root_id: UUID4 | None = None
    dt_created: datetime
    dt_updated: datetime

    class Config:
        orm_mode = True

class CategoryCreateRequest(BaseModel):
    name: str
    parent_id: UUID4 | None = None

class CategoryChilds(BaseModel):
    id: UUID4
    name: str
    parent_id: UUID4 | None = None
    root_id: UUID4 | None = None
    dt_created: datetime
    dt_updated: datetime

    class Config:
        orm_mode = True

class CategoryChildsRequest(BaseModel):
    category_id: UUID4

class CategoryChildrens(BaseModel):
    id: UUID4
    name: str
    children_count: int = 0

