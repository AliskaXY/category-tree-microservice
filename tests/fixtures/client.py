from pytest import fixture

from category_tree.db.models import Client

@fixture
async def ms_client(session):
    ms_client = Client(
        name = "Kuznetsov Bob Efimovich",
        email = "kuznetsov@gmail.com",
        address = "Moscow, Lenina, 1"
    )
    session.add(ms_client)
    await session.commit()
    await session.refresh(ms_client)
    return ms_client

