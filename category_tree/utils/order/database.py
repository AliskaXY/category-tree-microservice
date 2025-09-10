from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import *
from category_tree.db.models import Order, OrderItem, Product
from category_tree.schemas import AddOrderItemRequest, OrderStatusEnum


async def add_order_item(db: AsyncSession, item: AddOrderItemRequest):
    """
    Добавление товара в заказ
    В случае, если заказа еще не сформирован, создается новый заказ
    """

    try:
        product = await db.get(Product, item.product_id)
        if not product:
            raise ProductNotFoundError(f"Продукт с ID {item.product_id} не найден")
        if product.amount < item.amount:
            raise NotEnoughProductsError(f"Недостаточно {product.name} для заказа")

        order = await db.get(Order, item.order_id) if item.order_id else None
        if not order:
            if not item.client_id:
                raise NotEnoughInfoError("Не достаточно информации для создания заказа")
            order = Order(client_id=item.client_id, status=OrderStatusEnum.FORMING)
            db.add(order)
            await db.flush()
            order_item = None
        else:
            stmt = select(OrderItem).where(OrderItem.order_id == item.order_id, OrderItem.product_id == item.product_id)
            result = await db.execute(stmt)
            order_item = result.scalar_one_or_none()

        if order_item:
            order_item.amount += item.amount
            await db.flush()
        else:
            order_item = OrderItem(order_id=order.id, product_id=product.id, amount=item.amount)
            db.add(order_item)
        product.amount -= item.amount
        db.add(product)
        await db.commit()
        await db.refresh(order_item)
        return order_item

    except Exception as e:
        await db.rollback()
        raise e
