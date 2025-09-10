from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, and_

from category_tree.db.models import Client, Order, OrderItem

async def get_client_totals(db: AsyncSession):
    """2.1. Получение информации о сумме товаров заказанных под каждого клиента"""

    stmt = (
        select(
            Client.name,
            func.sum(OrderItem.amount).label('total_amount')
        )
        .join(
            Order, and_(
                Order.client_id == Client.id,
                Order.status == "done"
            )
        )
        .join(
            OrderItem, OrderItem.order_id == Order.id
        )
        .group_by(
            Client.id, Client.name
        )
    )
    
    result = await db.execute(stmt)
    return result.all()