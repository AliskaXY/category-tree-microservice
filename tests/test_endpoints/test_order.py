import pytest

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from category_tree.config import get_settings
from category_tree.db.models import OrderItem
from category_tree.schemas import AddOrderItemRequest


class TestOrder:
    @staticmethod
    def get_url() -> str:
        settings = get_settings()
        return settings.PATH_PREFIX + "/order"
    
    @pytest.mark.parametrize(
        "amount, stat, length",
        (
            (1, status.HTTP_201_CREATED, 1),
            (2, status.HTTP_201_CREATED, 1),
            (10, status.HTTP_400_BAD_REQUEST, 0)
        ),
    )
    async def test_add_item_with_client_id(self, client, session: AsyncSession, ms_client, product, amount, stat, length):
        order_item = AddOrderItemRequest(product_id=product.id, amount=amount, client_id=ms_client.id)
        response = await client.post(
            self.get_url() + "/add_item",
            json={
                "product_id": str(order_item.product_id),
                "amount": order_item.amount,
                "client_id": str(order_item.client_id)
            }
        )
        assert response.status_code == stat
        query = select(OrderItem).filter(
            and_(
                OrderItem.product_id == order_item.product_id,
                OrderItem.amount == order_item.amount
            )
        )
        assert len((await session.scalars(query)).all()) == length