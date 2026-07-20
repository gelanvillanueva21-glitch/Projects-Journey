from datetime import datetime, timedelta, timezone
from jose import jwt
from config import setting

import bcrypt


def hash_password(password : str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_pass(text_password : str, hashed_password : str) -> bool:
    return bcrypt.checkpw(
        text_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_jwt(data : dict, expires_delta : timedelta | None = None):
    encode_data = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=setting.access_token_expr))
    encode_data.update({"exp" : expire})
    return jwt.encode(
        encode_data, 
        setting.secret_key, 
        algorithm=setting.algorithm)




