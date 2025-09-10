from pytest import fixture

from category_tree.db.models import Product, ProductCategory


@fixture
async def product(session, category_tree):
    product = Product(name="LEX LWM06010BLIDSMALL", amount=3, price=35000)
    session.add(product)
    await session.flush()
    product_cat_root = ProductCategory(product_id=product.id, category_id=category_tree[0].id)
    product_cat_second = ProductCategory(product_id=product.id, category_id=category_tree[1].id)
    session.add(product_cat_root)
    session.add(product_cat_second)
    await session.commit()
    await session.refresh(product)
    return product