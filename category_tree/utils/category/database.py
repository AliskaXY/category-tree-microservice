from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from category_tree.db.models import Category

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