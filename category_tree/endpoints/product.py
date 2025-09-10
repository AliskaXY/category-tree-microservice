from fastapi import APIRouter, Body, Depends, Path, Request
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from category_tree.db.connection import get_session
from category_tree.schemas import MessageResponse
from category_tree.schemas import Product as ProductSchema
from category_tree.schemas import ProductCreateRequest, ProductTotalSold
from category_tree.utils.product import add_category_to_product, create_product, get_top_products_last_month


api_router = APIRouter(
    prefix="/product",
    tags=["Products"],
)


@api_router.post(
    "",
    response_model=ProductSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    _: Request,
    product: ProductCreateRequest = Body(...),
    session: AsyncSession = Depends(get_session),
):
    return await create_product(session, product)


@api_router.post(
    "/{product_id}/category/{category_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def category_to_product(
    _: Request,
    product_id: UUID4 = Path(...),
    category_id: UUID4 = Path(...),
    session: AsyncSession = Depends(get_session),
):
    await add_category_to_product(session, product_id, category_id)
    return {"message": "Category added to product"}


@api_router.get(
    "/top5_last_month",
    response_model=list[ProductTotalSold],
    status_code=status.HTTP_200_OK,
)
async def top_products_last_month(
    _: Request,
    session: AsyncSession = Depends(get_session),
):
    return await get_top_products_last_month(session)
