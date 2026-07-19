from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeingKey
from database import Base


class User(Base):
    __tablename__ = "users"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    email : Mapped[str] = mapped_column(
        String(255), 
        primary_key = True, 
        index = True)
    hashed_password : Mapped[str] = mapped_column(String(255))
    is_active : Mapped[bool] = mapped_column(default = True)
    
    tasks : Mapped[list["Task"]] = relationship(back_populates = "user")


class Task(Base):
    __tablename__ = "tasks"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    title : Mapped[str] = mapped_column(String(255))
    description : Mapped[str | None] = mapped_column(String(255))
    is_done : Mapped[bool] = mapped_column(default = False)
    user_id : Mapped[int] = mapped_column(ForeingKey("users.id"))
    
    user : Mapped["User"] = relationship(back_populates = "tasks")


