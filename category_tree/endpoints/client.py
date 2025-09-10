from fastapi import APIRouter, Body, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from category_tree.db.connection import get_session
from category_tree.schemas import Client as ClientSchema
from category_tree.schemas import ClientCreateRequest, ClientTotal
from category_tree.utils.client import create_client, get_clients_totals


api_router = APIRouter(
    prefix="/client",
    tags=["Clients"],
)


@api_router.post(
    "",
    response_model=ClientSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    _: Request,
    client: ClientCreateRequest = Body(...),
    session: AsyncSession = Depends(get_session),
):
    return await create_client(session, client)


@api_router.get(
    "/clients_totals",
    response_model=list[ClientTotal],
    status_code=status.HTTP_200_OK,
)
async def clients_totals(
    _: Request,
    session: AsyncSession = Depends(get_session),
):
    return await get_clients_totals(session)
