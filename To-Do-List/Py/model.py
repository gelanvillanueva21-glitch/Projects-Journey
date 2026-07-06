from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, SessionLocal

class UserAuthInfo(Base):
    __tablename__ = "users"
    
    id = Column(
        Integer, 
        primary_key = True,
        index = True)
    username = Column(
        String,
        unique = True,
        index = True
    )
    password = Column(String)
    todolist = relationship(
        "Todo", 
        back_populates = "owner", 
        cascade = "all, delete-orphan"
    )


class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(
        Integer,
        primary_key = True,
        index = True
    )
    title = Column(
        String,
        nullable = False
    )
    is_complete = Column(
        Boolean,
        default = False
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )
    owner = relationship(
        "UserAuthInfo", 
        back_populates = "todolist"
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()