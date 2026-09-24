from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app import models, schemas
from app.services.sms_parser import parse_sms
from app.services.categorizer import categorize_transaction

router = APIRouter(prefix="/sms", tags=["SMS"])


@router.post("/ingest")
def ingest_sms(payload: schemas.SMSInput, db: Session = Depends(get_db)):
    """
    Receives raw SMS text (from the Android app), runs it through the
    parser + categorizer, and stores it as a Transaction if it's a
    real transaction. Non-transactional SMS (OTP, promo, etc.) are
    detected and ignored.
    """
    parsed = parse_sms(payload.sms_text)

    if not parsed.is_transaction:
        return {"status": "ignored", "reason": "not a transactional SMS"}

    category = categorize_transaction(parsed.merchant or "", parsed.raw_text)

    transaction_date = datetime.strptime(parsed.date, "%Y-%m-%d").date()

    db_transaction = models.Transaction(
        amount=parsed.amount,
        merchant=parsed.merchant,
        date=transaction_date,
        payment_method=parsed.payment_method,
        transaction_type=parsed.transaction_type,
        category=category,
        raw_sms=parsed.raw_text,
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return {
        "status": "stored",
        "transaction": schemas.TransactionOut.model_validate(db_transaction),
    }