from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = f"sqlite:///../Data/users_info.db"

engine = create_engine(
    DATABASE_URL,
    connect_args = {"check_same_thread" : False}
    )

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)
Base = declarative_base()