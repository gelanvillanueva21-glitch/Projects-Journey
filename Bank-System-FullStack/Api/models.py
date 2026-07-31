from sqlalchemy import String, ForeignKey, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database import Base



class User(Base):
    __tablename__ = "users"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    email : Mapped[str] = mapped_column(String(225), unique = True, index = True)
    hashed_password : Mapped[str] = mapped_column(String(225))
    name : Mapped[str] = mapped_column(String(155))
    is_active : Mapped[bool] = mapped_column(default = True)
    can_lend : Mapped[bool] = mapped_column(default = False)
    anual_interest_rate : Mapped[int] = mapped_column(default = 0)
    amount_lend : Mapped[int] = mapped_column(default = 0)
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone = True), 
        server_default = func.now())
    available_balance : Mapped[int] = mapped_column(default = 0)
    
    loans : Mapped[list["Loan"]] = relationship(
        back_populates = "deptor_owner", 
        cascade = "all, delete-orphan",
        foreign_keys = "[Loan.debtor_id]")
    lender : Mapped[list["Loan"]] = relationship(
        back_populates = "lender_owner",
        foreign_keys = "[Loan.lender_id]")
    withdraws : Mapped[list["Withdraw"]] = relationship(
        back_populates = "withdraw_owner",
        cascade = "all, delete-orphan")
    deposits : Mapped[list["Deposit"]] = relationship(
        back_populates = "deposit_owner",
        cascade = "all, delete-orphan")
    loan_payment_history : Mapped[list["LoanPayment"]] = relationship(
        back_populates = "payment_owner",
        cascade = "all, delete-orphan",
        foreign_keys = "[LoanPayment.debtor_id]")
    lender_paid : Mapped[list["LoanPayment"]] = relationship(
        back_populates = "lender_owner",
        foreign_keys = "[LoanPayment.lender_id]")
    loan_archived : Mapped[list["LoanHistory"]] = relationship(
        back_populates = "owner",
        cascade = "all, delete-orphan",
        foreign_keys = "[LoanHistory.debtor_id]")
    lender_archived : Mapped[list["LoanHistory"]] = relationship(
        back_populates = "lender_history",
        foreign_keys = "[LoanHistory.lender_id]")



class Loan(Base):
    __tablename__ = "loans"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    debtor_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    lender_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    loaned_date : Mapped[datetime] = mapped_column(
        DateTime(timezone = False),
        server_default = func.now())
    due_date : Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default = None)
    monthly_due_date : Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default = None)
    monthly_pay : Mapped[int] = mapped_column(default = 12)
    loan_balance : Mapped[int]
    anual_interest_rate : Mapped[int]
    
    deptor_owner : Mapped["User"] = relationship(
        back_populates = "loans",
        foreign_keys = [debtor_id])
    lender_owner : Mapped["User"] = relationship(
        back_populates = "lender",
        foreign_keys = [lender_id])



class LoanPayment(Base):
    __tablename__ = "loanpayment"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    debtor_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    lender_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    paid_date : Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now())
    paid_amount : Mapped[int]
    
    payment_owner : Mapped["User"] = relationship(
        back_populates = "loan_payment_history",
        foreign_keys = [debtor_id])
    lender_owner : Mapped["User"] = relationship(
        back_populates = "lender_paid",
        foreign_keys = [lender_id])



class LoanHistory(Base):
    __tablename__ = "loan_archive"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    debtor_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    lender_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    paid_date : Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now())
    is_paid : Mapped[bool] = mapped_column(default = True)
    
    owner : Mapped["User"] = relationship(
        back_populates = "loan_archived",
        foreign_keys = [debtor_id])
    lender_history : Mapped["User"] = relationship(
        back_populates = "lender_archived",
        foreign_keys = [lender_id])



class Withdraw(Base):
    __tablename__ = "withdraws"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    date : Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now())
    withdraw_amount : Mapped[int]
    
    withdraw_owner : Mapped["User"] = relationship(
        back_populates = "withdraws")



class Deposit(Base):
    __tablename__ = "deposits"
    
    id : Mapped[int] = mapped_column(primary_key = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    date : Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now())
    deposit_balance : Mapped[int]
    
    deposit_owner : Mapped["User"] = relationship(back_populates = "deposits")






