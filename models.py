from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    merchant = Column(String, index=True)
    date = Column(Date, index=True)
    payment_method = Column(String)
    transaction_type = Column(String)   # "debit" or "credit"
    category = Column(String, index=True)
    raw_sms = Column(String)