from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from category_tree.config import get_settings
from category_tree.db.models import Category


class TestCategory:
    @staticmethod
    def get_url() -> str:
        settings = get_settings()
        return settings.PATH_PREFIX + "/category"
    
    async def test_create_category(self, client, session: AsyncSession):
        response = await client.post(
            self.get_url(),
            json={
                "name": "Test Category",
                "parent_id": None,
                "root_id": None
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Test Category"
        assert data["parent_id"] is None
        assert data["root_id"] is None
        query = select(Category).filter(
            and_(
                Category.name == "Test Category",
                Category.parent_id.is_(None),
                Category.root_id.is_(None),
            )
        )
        assert len((await session.scalars(query)).all()) == 1

    async def test_get_category_children_counts(self, client, session: AsyncSession, category_tree):
        response = await client.get(
            self.get_url() + "/children_counts"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        for ctegory in data:
            if ctegory["name"] in ("Бытовая техника", "Холодильники"):
                assert ctegory["children_count"] == 2
            else:
                assert ctegory["children_count"] == 0