from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database import Base



class User(Base):
    __tablename__ = "users"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    email : Mapped[str] = mapped_column(
        String(255),
        unique = True,
        index = True
    )
    hashed_password : Mapped[str] = mapped_column(String(255))
    is_active : Mapped[bool] = mapped_column(default = True)
    
    urls : Mapped["Url"] = relationship(back_populates = "user")



class Url(Base):
    __tablename__ = "urls"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    original_url : Mapped[str] = mapped_column(String(2048))
    short_code : Mapped[str] = mapped_column(
        String(12),
        unique = True,
        index = True)
    created_at : Mapped[datetime] = mapped_column(server_default = func.now())
    expires_at : Mapped[datetime | None] = mapped_column(default = None)
    
    user : Mapped["User"] = relationship(back_populates = "urls")
    click  : Mapped["Click"] = relationship(back_populates = "url")
    



class Click(Base):
    __tablename__ = "clicks"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    url_id : Mapped[int] = mapped_column(ForeignKey("urls.id"))
    clicked_at : Mapped[datetime] = mapped_column(server_default = func.now())
    ip_address : Mapped[str | None] = mapped_column(String(45), default=None)
    
    url : Mapped["Url"] = relationship(back_populates = "click")


