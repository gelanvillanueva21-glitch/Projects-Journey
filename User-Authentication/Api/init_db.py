import asyncio
from database import Engine, Base
from models import User, Task


async def create_tables():
    async with Engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())
    print("Table Created")


