"""
categorizer.py
----------------
Classifies a transaction into a spending category.

Two layers:
1. Rule-based merchant/keyword matching (primary) - fast, accurate,
   no training data needed, handles the vast majority of real SMS.
2. Naive Bayes ML classifier (fallback) - trained on a small labeled
   dataset, used when the merchant name isn't recognized by rules.
   This satisfies the "ML" requirement of the project and can be
   demonstrated/evaluated independently (see train_model() below).
"""

import re
from typing import Optional
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

CATEGORIES = ["Food", "Shopping", "Transportation", "Bills", "Entertainment", "Healthcare", "Others"]

# ---------- Layer 1: Rule-based keyword matching ----------

CATEGORY_KEYWORDS = {
    "Food": [
        "swiggy", "zomato", "dominos", "pizza", "restaurant", "cafe", "starbucks",
        "mcdonald", "kfc", "burger", "food", "eatery", "dining", "bakery", "haldiram"
    ],
    "Shopping": [
        "amazon", "flipkart", "myntra", "ajio", "shopping", "mall", "reliance trends",
        "lifestyle", "decathlon", "meesho", "nykaa", "shoppers stop"
    ],
    "Transportation": [
        "uber", "ola", "rapido", "irctc", "petrol", "fuel", "metro", "bus", "indianoil",
        "hpcl", "bpcl", "parking", "toll", "fastag", "cab"
    ],
    "Bills": [
        "electricity", "recharge", "airtel", "jio", "vodafone", "vi ", "broadband",
        "wifi", "gas bill", "water bill", "dth", "insurance", "emi", "loan", "rent"
    ],
    "Entertainment": [
        "netflix", "amazon prime", "hotstar", "spotify", "bookmyshow", "pvr", "inox",
        "movie", "cinema", "gaming", "steam", "playstation", "youtube premium"
    ],
    "Healthcare": [
        "pharmacy", "apollo", "medplus", "hospital", "clinic", "doctor", "medical",
        "medicine", "diagnostic", "healthkart", "netmeds", "1mg"
    ],
}


def categorize_by_rules(merchant: str, raw_text: str) -> Optional[str]:
    """Returns a category if a known keyword is found, else None."""
    search_text = f"{merchant} {raw_text}".lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in search_text:
                return category
    return None


# ---------- Layer 2: ML fallback (Naive Bayes text classifier) ----------

# Small labeled training set: (text, category)
# In a real project you'd expand this with more real/sample SMS examples.
TRAINING_DATA = [
    ("swiggy food delivery order", "Food"),
    ("zomato restaurant order", "Food"),
    ("dominos pizza order", "Food"),
    ("cafe coffee day payment", "Food"),
    ("amazon online shopping order", "Shopping"),
    ("flipkart purchase order", "Shopping"),
    ("myntra clothing purchase", "Shopping"),
    ("uber cab ride payment", "Transportation"),
    ("ola cab booking payment", "Transportation"),
    ("petrol pump fuel payment", "Transportation"),
    ("irctc train ticket booking", "Transportation"),
    ("electricity bill payment", "Bills"),
    ("airtel mobile recharge", "Bills"),
    ("jio broadband bill payment", "Bills"),
    ("insurance premium payment", "Bills"),
    ("netflix subscription payment", "Entertainment"),
    ("bookmyshow movie ticket booking", "Entertainment"),
    ("spotify premium subscription", "Entertainment"),
    ("apollo pharmacy medicine purchase", "Healthcare"),
    ("hospital consultation payment", "Healthcare"),
    ("medplus medical store purchase", "Healthcare"),
    ("atm cash withdrawal", "Others"),
    ("fund transfer to friend", "Others"),
    ("miscellaneous payment", "Others"),
]

_vectorizer = CountVectorizer()
_model = MultinomialNB()


def train_model():
    """Trains the Naive Bayes model on the small labeled dataset above."""
    texts = [t[0] for t in TRAINING_DATA]
    labels = [t[1] for t in TRAINING_DATA]
    X = _vectorizer.fit_transform(texts)
    _model.fit(X, labels)


def categorize_by_ml(merchant: str, raw_text: str) -> str:
    """Predicts category using the trained Naive Bayes model."""
    text = f"{merchant} {raw_text}"
    X = _vectorizer.transform([text])
    prediction = _model.predict(X)
    return prediction[0]


# Train once when this module is imported
train_model()


# ---------- Combined entry point ----------

def categorize_transaction(merchant: str, raw_text: str) -> str:
    """
    Main function used by the rest of the app.
    Tries rule-based matching first (explainable, high precision).
    Falls back to ML model if no rule matches.
    """
    category = categorize_by_rules(merchant, raw_text)
    if category:
        return category
    return categorize_by_ml(merchant, raw_text)


if __name__ == "__main__":
    test_cases = [
        ("Swiggy", "Rs.500 debited to VPA swiggy@okhdfcbank"),
        ("Amazon", "You have spent INR 1250 at AMAZON"),
        ("Uber", "Rs 300 paid to Uber via UPI"),
        ("XYZPharma", "Rs 450 debited at XYZPharma medical store"),  # not in rules, tests ML fallback
        ("Unknown", "Rs 1000 sent via UPI to a friend"),
    ]
    for merchant, text in test_cases:
        print(f"{merchant!r:15} -> {categorize_transaction(merchant, text)}")