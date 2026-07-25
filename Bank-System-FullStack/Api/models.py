from sqlalchemy import String, ForeignKey, func, DateTime, DECIMAL
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
    can_lend : Mapped[bool] = mapped_column(default = False)
    monthly_payment_amount : Mapped[DECIMAL] = mapped_column(default = 0.00)
    anual_interest_rate : Mapped[int] = mapped_column(default = 0)
    amount_lend : Mapped[int] = mapped_column(default = 0)
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone = True), 
        server_default = func.now())
    availabe_balance : Mapped[int] = mapped_column(default = 0)
    
    loans : Mapped[list["Loan"]] = relationship(back_populates = "owner")
    withdraws : Mapped[list["Withdraw"]] = relationship(back_populates = "owner")
    deposits : Mapped[list["Deposit"]] = relationship(back_populates = "owner")
    loan_payment_history = Mapped[list["LoanPayment"]] = relationship(back_populates = "owner")



class Loan(Base):
    __tablename__ = "loans"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    debtor_id : Mapped[int]
    lender_id : Mapped[int]
    loaned_date : Mapped[datetime] = mapped_column(
        DateTime(timezone = False),
        server_default = func.now())
    due_date : Mapped[datetime | None] = mapped_column(default = None)
    monthly_due_date : Mapped[datetime | None] = mapped_column(default = None)
    loan_balance : Mapped[int]
    anual_interest_rate : Mapped[int]
    is_paid : Mapped[bool] = mapped_column(default = False)
    
    owner : Mapped["User"] = relationship(back_populates = "loans")



class LoanPayment(Base):
    __tablename__ = "loanpayment"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    deptor_id : Mapped[int]
    lender_id : Mapped[int]
    paid_date : Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now())
    paid_amount : Mapped[int]
    
    owner : Mapped["User"] = relationship(back_populates = "loan_payment_history")



class Withdraw(Base):
    __tablename__ = "withdraws"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    date : Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now())
    withdraw_balance : Mapped[int]
    
    owner : Mapped["User"] = mapped_column(relationship(back_populates = "withdraws"))



class Deposit(Base):
    __tablename__ = "deposits"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    user_id : Mapped[int]
    date : Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now())
    deposit_balance : Mapped[int]
    
    owner = Mapped["User"] = relationship(back_populates = "deposits")






