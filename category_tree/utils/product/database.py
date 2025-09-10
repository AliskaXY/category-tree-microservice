from datetime import datetime, timedelta, timezone

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from category_tree.db.models import Category, Order, OrderItem, Product, ProductCategory
from category_tree.schemas import ProductCreateRequest


async def create_product(db: AsyncSession, product: ProductCreateRequest):
    """Создание товара"""
    product = Product(name=product.name, price=product.price, amount=product.amount)
    db.add(product)
    await db.commit()
    return product


async def add_category_to_product(db: AsyncSession, product_id: int, category_id: int):
    """Добавление категории к товару"""
    product_category = ProductCategory(product_id=product_id, category_id=category_id)
    db.add(product_category)
    await db.commit()
    return product_category


async def get_top_products_last_month(db: AsyncSession):
    """2.3.1. Топ-5 самых покупаемых товаров за последний месяц"""
    one_month_ago = datetime.now(timezone.utc) - timedelta(days=30)

    stmt = (
        select(
            Product.name.label("product_name"),
            Category.name.label("root_category_name"),
            func.sum(OrderItem.amount).label("total_sold"),
        )
        .join(OrderItem, OrderItem.product_id == Product.id)
        .join(Order, OrderItem.order_id == Order.id)
        .join(ProductCategory, ProductCategory.product_id == Product.id)
        .join(Category, Category.id == ProductCategory.category_id)
        .where(
            and_(
                Order.dt_created >= one_month_ago,
                Order.status == "done",
                Category.parent_id.is_(None),  # Категории первого уровня
            )
        )
        .group_by(Product.id, Category.id)
        .order_by(func.sum(OrderItem.amount).desc())
        .limit(5)
    )

    result = await db.execute(stmt)
    return result.all()
