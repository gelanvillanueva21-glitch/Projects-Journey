from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings


class Base(DeclarativeBase): pass
engine = create_async_engine(
    settings.database_url,
    pool_size = 5,
    max_overflow = 7,
    pool_pre_ping = True
)


async_session_local = async_sessionmaker(
    engine,
    class_ = AsyncSession,
    expire_on_commit = False,
    autocommit = False,
    autoflush = False
)


async def get_database():
    async with async_session_local() as session:
        yield session


