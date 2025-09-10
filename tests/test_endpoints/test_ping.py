from os import environ

import pytest
from starlette import status

from category_tree.config.utils import get_settings
from category_tree.db.connection import SessionManager


API_URL = get_settings().PATH_PREFIX + "/health_check"

@pytest.mark.asyncio
async def test_ping_application(client):
    url = API_URL + "/ping_application"
    response = await client.get(url=url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_ping_database(client):
    url = API_URL + "/ping_database"
    response = await client.get(url=url)
    assert response.status_code == status.HTTP_200_OK


@pytest.fixture(scope="function")
def wrong_postgres_port():
    settings = get_settings()
    old_port = settings.POSTGRES_PORT
    environ["POSTGRES_PORT"] = str(old_port + 1)
    manager = SessionManager()
    manager.refresh()
    yield
    environ["POSTGRES_PORT"] = str(old_port)

@pytest.mark.asyncio
# pylint: disable=redefined-outer-name, unused-argument
async def test_ping_database_fail(client, wrong_postgres_port):
    url = API_URL + "/ping_database"
    response = await client.get(url=url)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
# pylint: enable=redefined-outer-name, unused-argument
