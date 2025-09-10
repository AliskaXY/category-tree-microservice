from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from category_tree.db.models import Category
from category_tree.schemas import CategoryCreateRequest

async def create_category(db: AsyncSession, category: CategoryCreateRequest):
    """Создание категории"""
    if category.parent_id is not None:
        parent = await db.get(Category, category.parent_id)
        if parent.root_id is not None:
            category = Category(name=category.name, parent_id=category.parent_id, root_id=parent.root_id)
        else:
            category = Category(name=category.name, parent_id=category.parent_id, root_id=category.parent_id)      
    else:
        category = Category(name=category.name)
    db.add(category)
    await db.commit()
    return category

async def get_category_children_counts(db: AsyncSession):
    """2.2. Количество дочерних элементов первого уровня для категорий"""

    parent = aliased(Category)
    child = aliased(Category)

    stmt = select(
        parent.id,
        parent.name,
        func.count(child.id).label('children_count')
    ).outerjoin(
        child, child.parent_id == parent.id
    ).group_by(
        parent.id, parent.name
    )

    resault = await db.execute(stmt)
    return resault.all()