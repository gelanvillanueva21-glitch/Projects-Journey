from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from Config.config import settings



# This is our Base to use this in the models
# purpose for the tables
# Added AsyncAttrs in the Base, so we can fetch
# data that has a relationship using await
class Base(AsyncAttrs, DeclarativeBase): pass
engine = create_async_engine(
    settings.database_url,
    pool_size = 5,
    max_overflow = 10,
    pool_pre_ping = True
)


# Creating variable async session to maintain the code clean
# when it comes to the get database function
# this is our factory to connect the engine to the database
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



