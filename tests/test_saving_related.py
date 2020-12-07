from typing import Union

import databases
import ormar
import pytest
import sqlalchemy as sa

from tests.settings import DATABASE_URL

engine = sa.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = sa.MetaData()
db = databases.Database(DATABASE_URL)


class Category(ormar.Model):
    class Meta:
        tablename = "categories"
        metadata = metadata
        database = db

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=50, unique=True, index=True)
    code: int = ormar.Integer()


class Workshop(ormar.Model):
    class Meta:
        tablename = "workshops"
        metadata = metadata
        database = db

    id: int = ormar.Integer(primary_key=True)
    topic: str = ormar.String(max_length=255, index=True)
    category: Union[ormar.Model, Category] = ormar.ForeignKey(
        Category, related_name="workshops", nullable=False
    )


@pytest.fixture
def create_test_database():
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)


@pytest.mark.asyncio
async def test_model_relationship(create_test_database):
    cat = await Category(name="Foo", code=123).save()
    ws = await Workshop(topic="Topic 1", category=cat).save()

    assert ws.id == 1
    assert ws.topic == "Topic 1"
    assert ws.category.name == "Foo"
