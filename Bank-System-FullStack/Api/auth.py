from datetime import datetime, timedelta, timezone
from jose import jwt
from Config.config import settings
import bcrypt



def hash_password(password :str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")



def verify_password(text_password : str, hashed_password : str) -> bool:
    return bcrypt.checkpw(
        text_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )



def create_jwt(data : dict, expires_delta : timedelta | None = None):
    copy_data = data.copy()
    expired_at = datetime.now(timezone.utc) + (
        expires_delta or timedelta(
            minutes = settings.access_token_expire_hour))
    copy_data.update({"exp" : expired_at})
    return jwt.encode(
        copy_data,
        settings.secret_key,
        algorithm=settings.algorithm
    )




