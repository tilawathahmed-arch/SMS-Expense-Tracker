from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/transactions", response_model=List[schemas.TransactionOut])
def get_all_transactions(db: Session = Depends(get_db)):
    """Returns all stored transactions, most recent first."""
    transactions = (
        db.query(models.Transaction)
        .order_by(models.Transaction.date.desc())
        .all()
    )
    return transactions


@router.get("/summary/category")
def get_category_summary(db: Session = Depends(get_db)):
    """
    Returns total spend per category, e.g.:
    [{"category": "Food", "total": 1500.0}, {"category": "Shopping", "total": 3200.0}, ...]
    Used for the pie chart. Only counts debits (money spent), not credits.
    """
    results = (
        db.query(models.Transaction.category, func.sum(models.Transaction.amount))
        .filter(models.Transaction.transaction_type == "debit")
        .group_by(models.Transaction.category)
        .all()
    )
    return [{"category": category, "total": total} for category, total in results]


@router.get("/summary/monthly")
def get_monthly_summary(db: Session = Depends(get_db)):
    """
    Returns total spend per month, e.g.:
    [{"month": "2026-07", "total": 4500.0}, {"month": "2026-08", "total": 3100.0}, ...]
    Used for the bar chart. Only counts debits.
    """
    results = (
        db.query(
            extract("year", models.Transaction.date).label("year"),
            extract("month", models.Transaction.date).label("month"),
            func.sum(models.Transaction.amount).label("total"),
        )
        .filter(models.Transaction.transaction_type == "debit")
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )
    return [
        {"month": f"{int(year)}-{int(month):02d}", "total": total}
        for year, month, total in results
    ]


@router.get("/summary/totals")
def get_totals(db: Session = Depends(get_db)):
    """Quick overview: total spent, total credited, transaction count."""
    total_spent = (
        db.query(func.sum(models.Transaction.amount))
        .filter(models.Transaction.transaction_type == "debit")
        .scalar() or 0
    )
    total_credited = (
        db.query(func.sum(models.Transaction.amount))
        .filter(models.Transaction.transaction_type == "credit")
        .scalar() or 0
    )
    count = db.query(func.count(models.Transaction.id)).scalar() or 0

    return {
        "total_spent": total_spent,
        "total_credited": total_credited,
        "transaction_count": count,
    }