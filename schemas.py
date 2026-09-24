from pydantic import BaseModel
from datetime import date as date_type
from typing import Optional


class SMSInput(BaseModel):
    """What the Android app (or Postman/test) sends to the backend."""
    sms_text: str
    sender: Optional[str] = None


class TransactionOut(BaseModel):
    """What the API returns for a single transaction."""
    id: int
    amount: float
    merchant: Optional[str]
    date: date_type
    payment_method: Optional[str]
    transaction_type: Optional[str]
    category: str

    class Config:
        from_attributes = True   # allows conversion from SQLAlchemy model -> Pydantic