import re
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

@dataclass
class ParsedTransaction:
    amount: Optional[float]
    merchant: Optional[str]
    date: Optional[str]
    payment_method: Optional[str]
    transaction_type: Optional[str]
    raw_text: str
    is_transaction: bool

AMOUNT_PATTERNS = [
    r"(?:rs\.?|inr)\s*([\d,]+\.?\d*)",
    r"([\d,]+\.?\d*)\s*(?:rs\.?|inr)",
]

DATE_PATTERNS = [
    r"(\d{1,2}[-/][A-Za-z]{3}[-/]\d{2,4})",
    r"(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})",
]

MERCHANT_PATTERNS = [
    r"(?:to|at)\s+(?:vpa\s+)?([A-Za-z0-9@._\-]+?)(?:\s+on|\s+ref|\.|\s*$)",
    r"info[:\-]\s*([A-Za-z0-9@._\- ]+?)(?:\s+on|\.|\s*$)",
]

PAYMENT_METHOD_KEYWORDS = {
    "UPI": ["upi", "vpa"],
    "Card": ["card", "credit card", "debit card"],
    "NetBanking": ["netbanking", "net banking", "imps", "neft", "rtgs"],
    "Wallet": ["wallet", "paytm wallet", "amazon pay balance"],
}

DEBIT_KEYWORDS = ["debited", "spent", "paid", "purchase", "withdrawn", "sent"]
CREDIT_KEYWORDS = ["credited", "received", "refund", "deposited"]
TRANSACTION_INDICATOR_KEYWORDS = DEBIT_KEYWORDS + CREDIT_KEYWORDS + ["a/c", "acct", "account"]
NON_TRANSACTION_KEYWORDS = ["otp", "one time password", "do not share", "offer", "cashback offer", "sale is live"]

def _extract_amount(text):
    for pattern in AMOUNT_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1).replace(",", ""))
            except ValueError:
                continue
    return None

def _extract_date(text):
    for pattern in DATE_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw_date = match.group(1)
            for fmt in ("%d-%b-%y", "%d-%b-%Y", "%d/%m/%y", "%d/%m/%Y", "%d-%m-%y", "%d-%m-%Y"):
                try:
                    return datetime.strptime(raw_date, fmt).date().isoformat()
                except ValueError:
                    continue
    return datetime.today().date().isoformat()

def _extract_merchant(text):
    for pattern in MERCHANT_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            merchant = match.group(1).strip(" .")
            merchant = re.sub(r"@ok[a-z]+bank", "", merchant, flags=re.IGNORECASE)
            merchant = re.sub(r"@[a-z]+", "", merchant, flags=re.IGNORECASE)
            if merchant and len(merchant) > 1:
                return merchant.title()
    return None

def _extract_payment_method(text):
    lowered = text.lower()
    for method, keywords in PAYMENT_METHOD_KEYWORDS.items():
        if any(kw in lowered for kw in keywords):
            return method
    return "Unknown"

def _extract_transaction_type(text):
    lowered = text.lower()
    if any(kw in lowered for kw in DEBIT_KEYWORDS):
        return "debit"
    if any(kw in lowered for kw in CREDIT_KEYWORDS):
        return "credit"
    return None

def is_transactional_sms(text):
    lowered = text.lower()
    if any(kw in lowered for kw in NON_TRANSACTION_KEYWORDS):
        return False
    return any(kw in lowered for kw in TRANSACTION_INDICATOR_KEYWORDS)

def parse_sms(text: str) -> ParsedTransaction:
    if not is_transactional_sms(text):
        return ParsedTransaction(None, None, None, None, None, text, False)

    amount = _extract_amount(text)
    date = _extract_date(text)
    merchant = _extract_merchant(text)
    payment_method = _extract_payment_method(text)
    transaction_type = _extract_transaction_type(text)

    return ParsedTransaction(
        amount=amount,
        merchant=merchant or "Unknown",
        date=date,
        payment_method=payment_method,
        transaction_type=transaction_type or "debit",
        raw_text=text,
        is_transaction=amount is not None,
    )

if __name__ == "__main__":
    samples = [
        "Rs.500.00 debited from A/c XX1234 on 12-07-26 to VPA swiggy@okhdfcbank. Ref No 123456789. -HDFC Bank",
        "You have spent INR 1,250.00 on your HDFC Bank Card XX1234 at AMAZON on 27-Jul-26",
        "Rs 200 debited via UPI on 28-07-2026 to ZOMATO. Not you? Call 1800xxx",
        "Your OTP for login is 4532. Do not share with anyone.",
        "Rs.15000 credited to your account XX1234 on 01-08-2026 by NEFT from EMPLOYER PVT LTD",
    ]
    for s in samples:
        print(parse_sms(s))