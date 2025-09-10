from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from category_tree.db.connection import get_session
from category_tree.schemas import Category as CategoryShema, CategoryCreateRequest, CategoryChildrens
from category_tree.utils.category import create_category, get_category_children_counts

api_router = APIRouter(
    prefix="/category",
    tags=["Products Categories"],
)

@api_router.post(
    "",
    response_model=CategoryShema,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    _: Request,
    category: CategoryCreateRequest = Body(...),
    session: AsyncSession = Depends(get_session),
):
    return await create_category(session, category)

@api_router.get(
    "/children_counts",
    response_model=list[CategoryChildrens],
    status_code=status.HTTP_200_OK,
)
async def category_children_counts(
    _: Request,
    session: AsyncSession = Depends(get_session),
):
    return await get_category_children_counts(session)