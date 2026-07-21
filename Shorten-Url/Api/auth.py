from datetime import datetime, timedelta, timezone
from jose import jwt
from config import settings
import bcrypt



def hash_password(password : str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(
    plain_password : str,
    hashed_password : str
) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )


def create_jwt(data : dict, expires_delta : timedelta | None = None):
    data_encoded = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes = settings.access_token_expire_minutes))
    data_encoded.update({"exp" : expire})
    return jwt.encode(
        data_encoded,
        settings.secret_key,
        algorithm=settings.algorithm)



