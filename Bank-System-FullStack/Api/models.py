from sqlalchemy import String, ForeignKey, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database import Base



class User(Base):
    __tablename__ = "users"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    email : Mapped[str] = mapped_column(String(225), unique = True, index = True)
    hashed_password : Mapped[str] = mapped_column(String(150))
    name : Mapped[str] = mapped_column(String(155))
    is_active : Mapped[bool] = mapped_column(default = True)
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone = True), 
        server_default = func.now())
    money : Mapped[int] = mapped_column(default = 0)
    
    loans : Mapped[list["Loan"]] = relationship(back_populates = "owner")
    withdraws : Mapped[list["Withdraw"]] = relationship(back_populates = "owner")



class Loan(Base):
    __tablename__ = "loans"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    loan_name : Mapped[str] = mapped_column(String(155))
    date : Mapped[datetime] = mapped_column(
        DateTime(timezone = False),
        server_default = func.now())
    laon_value : Mapped[datetime]
    
    owner : Mapped["User"] = relationship(back_populates = "loans")



class Withdraw(Base):
    __tablename__ = "withdraws"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    date : Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now())
    money : Mapped[int]
    
    owner : Mapped["User"] = mapped_column(relationship(back_populates = "withdraws"))




