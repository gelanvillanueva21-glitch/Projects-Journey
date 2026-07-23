from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User, Url, Click
from schemas import CreateUser, UrlCreate
from auth import hash_password
import secrets
import string


ALPHABET = string.ascii_letters + string.digits


def generate_short_code(length=6):
    return "".join(secrets.choice(ALPHABET) for _ in range(length))



async def get_url_db(
    database : AsyncSession,
    short_code : str
) -> Url | None:
        result = await database.execute(select(Url).where(Url.short_code == short_code))
        return result.scalar_one_or_none()


async def get_user_email(
    database : AsyncSession,
    email : str
) -> User | None:
        result = await database.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()



async def create_user(
    database : AsyncSession,
    user : CreateUser
) -> User:
        hash_pass = hash_password(user.password)
        user_data = User(
            email = user.email,
            hashed_password = hash_pass
        )
        database.add(user_data)
        await database.commit()
        await database.refresh(user_data)
        return user_data



async def create_url(
    database : AsyncSession,
    url_data : UrlCreate,
    user_id : int
) -> Url:
        short_code = None
        if url_data.custom_code:
            exist = await get_url_db(database, url_data.custom_code)
            if exist:
                raise ValueError(f"Short code '{url_data.custom_code}' already taken")
            short_code = url_data.custom_code
        else:
            while True:
                short_code = generate_short_code()
                exist = await get_url_db(database, short_code)
                if exist:
                    break
        db_url = Url(
            user_id = user_id,
            original_url = url_data.original_url,
            short_code = short_code,
            expires_at = url_data.expires_at
        )
        database.add(db_url)
        await database.commit()
        await database.refresh(db_url)
        return db_url



async def get_urls_by_user(
    database : AsyncSession,
    user_id : int
) -> list[Url]:
        result = await database.execute(select(Url).where(Url.user_id == user_id))
        return result.scalars().all()



async def record_click(
    database : AsyncSession,
    url_id : int,
    ip_address : str | None
) -> Click:
        db_click = Click(url_id = url_id, ip_address = ip_address)
        database.add(db_click)
        await database.commit()
        await database.refresh(db_click)
        return db_click



