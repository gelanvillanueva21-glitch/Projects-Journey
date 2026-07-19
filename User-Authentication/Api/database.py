from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import setting


class Base(DeclarativeBase): pass
Engine = create_async_engine(
    setting.database_url,
    echo = True,
    pool_size = 5,
    max_overflow = 10,
    pool_pre_ping = True
)


AsyncSessionLocal = async_sessionmaker(
    Engine,
    class_ = AsyncSession,
    expire_on_commit = False,
    autocommit = False,
    autoflush = False
)


async def get_database():
    async with AsyncSessionLocal() as session:
        yield session

