from pytest import fixture

from category_tree.db.models import Category


@fixture
async def category_tree(session):
    categories = []

    # Создание корневой категории
    root_category = Category(name="Бытовая техника")
    session.add(root_category)
    await session.flush()
    categories.append(root_category)

    # Создание категорий 1 уровня
    category_depth_1_1 = Category(name="Стиральные машины", parent_id=root_category.id, root_id=root_category.id)
    session.add(category_depth_1_1)
    category_depth_1_2 = Category(name="Холодильники", parent_id=root_category.id, root_id=root_category.id)
    session.add(category_depth_1_2)
    await session.flush()
    categories.append(category_depth_1_1)
    categories.append(category_depth_1_2)

    # Создание категорий 2 уровня (только для одной из ктегорий 1 уровня)
    category_depth_2_1 = Category(name="Однокамерные", parent_id=category_depth_1_2.id, root_id=root_category.id)
    session.add(category_depth_2_1)
    category_depth_2_2 = Category(name="Двукамерные", parent_id=category_depth_1_2.id, root_id=root_category.id)
    session.add(category_depth_2_2)
    await session.flush()
    categories.append(category_depth_2_1)
    categories.append(category_depth_2_2)

    await session.commit()
    for category in categories:
        await session.refresh(category)
    return categories