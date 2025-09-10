from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import aliased

from category_tree.db.models import Order, OrderItem, Product, ProductCategory, Category

async def get_top_products_last_month(db: AsyncSession):
    """2.3.1. Топ-5 самых покупаемых товаров за последний месяц"""
    one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)

    RootCategory = aliased(Category)
    
    stmt = (
        select(
            Product.name.label("product_name"),
            RootCategory.name.label("root_category_name"),
            func.sum(OrderItem.amount).label("total_sold")
        )
        .join(OrderItem, OrderItem.product_id == Product.id)
        .join(Order, and_(
            OrderItem.order_id == Order.id,
            Order.status == "done",
        ))
        .join(ProductCategory, ProductCategory.product_id == Product.id)
        .join(Category, Category.id == ProductCategory.category_id)
        .join(RootCategory, RootCategory.id == Category.root_id)
        .where(and_(
            Order.dt_created >= one_month_ago,
            RootCategory.parent_id.is_(None)  # Категории первого уровня
        ))
        .group_by(Product.id, RootCategory.id)
        .order_by(func.sum(OrderItem.amount).desc())
        .limit(5)
    )
    
    result = await db.execute(stmt)
    return result.all()