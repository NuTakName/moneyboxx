from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

debug = settings["debug"]["value"]

url = settings["db"]["test_url"] if debug else settings["db"]["url"]

async_engine = create_async_engine(
    url=url,
    pool_use_lifo=True,
)

async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)