from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from category_tree.db.models import Client, Order, OrderItem
from category_tree.schemas import ClientCreateRequest


async def create_client(db: AsyncSession, client: ClientCreateRequest):
    """Создание клиента"""
    client = Client(name=client.name, email=client.email, address=client.address)
    db.add(client)
    await db.commit()
    return client


async def get_clients_totals(db: AsyncSession):
    """2.1. Получение информации о сумме товаров заказанных под каждого клиента"""

    stmt = (
        select(Client.name, func.sum(OrderItem.amount).label("total_amount"))
        .join(Order, and_(Order.client_id == Client.id, Order.status == "done"))
        .join(OrderItem, OrderItem.order_id == Order.id)
        .group_by(Client.id, Client.name)
    )

    result = await db.execute(stmt)
    return result.all()
