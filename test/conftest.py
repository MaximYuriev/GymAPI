from typing import AsyncIterable

import pytest
from beanie import init_beanie
from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient

from src.config import config
from src.infrastruction.db.models.customer import CustomerModel
from src.infrastruction.db.models.ticket import TicketModel, TicketTypeModel


@pytest.fixture(scope="session")
def faker() -> Faker:
    return Faker('ru-RU')


@pytest.fixture(scope="session")
def motor_client() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(
        config.mongodb.url,
        connectTimeoutMS=3000,
    )
    return client


@pytest.fixture
async def prepare_database(motor_client):
    await init_beanie(
        database=motor_client.get_database(config.mongodb.db_name),
        document_models=[
            TicketModel,
            CustomerModel,
            TicketTypeModel,
        ],
    )
    yield
    await motor_client.drop_database(config.mongodb.db_name)
