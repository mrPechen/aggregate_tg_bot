import asyncio
from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient

from tgbot.config import DbConfig, load_config, Config


async def get_mongo_collection(config: DbConfig):
    uri = config.construct_mongo_url()
    client = AsyncIOMotorClient(uri)
    db = client[config.db]
    collection = db[config.collection]
    return collection


@asynccontextmanager
async def get_session():
    config: Config = await asyncio.to_thread(load_config)
    collection = await get_mongo_collection(config.db)
    try:
        yield collection
    finally:
        collection.database.client.close()
