from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from category_tree.config import get_settings
from category_tree.db.models import Client


class TestClient:
    @staticmethod
    def get_url() -> str:
        settings = get_settings()
        return settings.PATH_PREFIX + "/client"

    async def test_create_client(self, client, session: AsyncSession):
        response = await client.post(
            self.get_url(),
            json={
                "name": "John Doe",
                "email": "johndoe@example.com",
                "address": "123 Main St",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "johndoe@example.com"
        assert data

        query = select(Client).filter(
            and_(
                Client.name == "John Doe",
                Client.email == "johndoe@example.com",
                Client.address == "123 Main St",
            )
        )

        assert len((await session.scalars(query)).all()) == 1