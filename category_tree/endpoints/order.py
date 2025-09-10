from fastapi import APIRouter, Request, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from category_tree.db.connection.session import get_session
from category_tree.utils.order import add_order_item, ProductNotFoundError, NotEnoughProductsError, NotEnoughInfoError
from category_tree.schemas import AddOrderItemRequest, OrderItem as OrderItemShema

router = APIRouter(prefix="/orders", tags=["orders"])

api_router = APIRouter(
    prefix="/order",
    tags=["Orders"],
)

@api_router.post(
    "/add_item",
    response_model=OrderItemShema,
    status_code=status.HTTP_201_CREATED,
)
async def add(
    _: Request,
    order: AddOrderItemRequest = Body(...),
    session: AsyncSession = Depends(get_session),
):
    try:
        item = await add_order_item(session, order)
    except (ProductNotFoundError, NotEnoughInfoError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NotEnoughProductsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return item