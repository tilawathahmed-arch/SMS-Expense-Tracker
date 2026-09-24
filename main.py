from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import sms,dashboard

# Creates the tables (transactions) in expenses.db if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-Powered SMS Expense Tracker")

# Allow the React frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for development only; restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sms.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"message": "SMS Expense Tracker API is running"}