from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings


class Base(DeclarativeBase): pass
Engine = create_async_engine(
    settings.database_url,
    pool_size = 5,
    max_overflow = 7,
    pool_pre_ping = True
)


LocalSession = async_sessionmaker(
    Engine,
    class_ = AsyncSession,
    expire_on_commit = False,
    autocommit = False,
    autoflush = False
)

