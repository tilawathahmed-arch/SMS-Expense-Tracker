# 📱 SMS Expense Tracker

An Android-based expense management system that automatically processes transaction SMS messages and converts them into structured financial records. The system captures SMS on Android, sends transaction data to a FastAPI backend, extracts important details, categorizes expenses, stores them in SQLite, and displays spending information through a React dashboard.

## 📌 Problem Statement

Transaction messages from banks and payment services contain useful information such as amount, merchant, date, payment method, and debit/credit type. Manually recording these transactions is repetitive and can lead to missed or inconsistent expense records.

The **SMS Expense Tracker** automates this process by converting transaction SMS messages into organized expense records.

## 🎯 Objectives

* Capture transaction-related SMS messages from an Android device.
* Filter out OTPs, promotional messages, and unrelated SMS.
* Extract amount, merchant, date, payment method, and transaction type.
* Categorize expenses automatically.
* Store normalized transaction records in a database.
* Provide a dashboard for viewing expenses, summaries, and transaction history.

## ✨ Features

* Android SMS capture
* Automatic transaction SMS filtering
* Transaction field extraction
* Rule-based expense categorization
* Machine-learning-based categorization fallback
* SQLite database storage
* REST API integration
* React-based dashboard
* Category-wise expense visualization
* Monthly spending summaries
* Recent transaction history

## 🏗️ System Architecture

```text
Android Client
      ↓
SMS Capture
      ↓
FastAPI Backend
      ↓
SMS Filtering & Parsing
      ↓
Expense Categorization
      ↓
SQLite Database
      ↓
React Dashboard
```

### Main Components

**Android Application**

* Kotlin
* SMS permissions
* BroadcastReceiver
* OkHttp

**Backend**

* FastAPI
* Pydantic
* Python
* REST APIs

**Database**

* SQLite
* SQLAlchemy ORM

**Frontend**

* React
* Axios
* Recharts

**Machine Learning**

* CountVectorizer
* Multinomial Naive Bayes

## 🔄 Project Workflow

1. The Android application receives an SMS.
2. The SMS is forwarded to the FastAPI backend.
3. The backend validates and filters the message.
4. Transaction information is extracted using text-processing rules and regular expressions.
5. Expense categories are identified using rules first.
6. When no matching rule is found, Multinomial Naive Bayes is used as a fallback classifier.
7. The transaction is stored in SQLite.
8. The React dashboard retrieves the stored information through REST APIs.
9. Users can view totals, charts, and recent transactions.

## 🤖 Machine Learning Component

The project uses **Multinomial Naive Bayes** as a fallback method for expense categorization.

The SMS text is converted into numerical features using **CountVectorizer**, after which the classifier predicts categories such as:

* Food
* Shopping
* Transportation
* Bills
* Entertainment
* Healthcare
* Others

A rule-based layer is used first for known merchants and keywords, while the machine-learning model handles messages that do not match configured rules.

## 🗄️ Database

The project uses **SQLite** for lightweight local persistence and **SQLAlchemy** as the Object-Relational Mapping (ORM) layer.

Each transaction stores information such as:

```text
ID
Amount
Merchant
Date
Payment Method
Transaction Type
Category
Raw SMS
```

## 🌐 REST APIs

The React dashboard communicates with the FastAPI backend using REST endpoints.

Example endpoints:

```text
GET /dashboard/transactions
GET /dashboard/summary/category
GET /dashboard/summary/monthly
GET /dashboard/summary/totals
POST /sms/ingest
```

## 📊 Dashboard

The React dashboard provides:

* Total amount spent
* Total amount credited
* Transaction count
* Category-wise expense chart
* Monthly expense chart
* Recent transaction history

## 🛠️ Technologies Used

| Component        | Technologies                             |
| ---------------- | ---------------------------------------- |
| Mobile           | Android, Kotlin                          |
| Backend          | Python, FastAPI                          |
| Database         | SQLite, SQLAlchemy                       |
| Frontend         | React, Axios                             |
| Charts           | Recharts                                 |
| Machine Learning | Multinomial Naive Bayes, CountVectorizer |
| Communication    | REST API                                 |

## 📂 Project Structure

```text
sms-expense-tracker/
│
├── android/
│   └── SMS Expense Tracker Android application
│
├── backend/
│   └── FastAPI backend and SMS processing
│
├── frontend/
│   └── React dashboard
│
├── README.md
└── .gitignore
```

## ▶️ How to Run

### Backend

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Start the FastAPI server using the project's configured startup command.

### Frontend

Install dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

### Android

Open the Android project in Android Studio, configure the emulator/device, grant the required SMS permissions, and run the application.

For an Android emulator, the backend hosted on the development machine can be accessed using the configured host address.

## 🧪 Testing

The project was tested for:

* SMS permission handling
* Transaction SMS filtering
* Transaction field extraction
* Expense categorization
* Database persistence
* REST API communication
* React dashboard display

## ⚠️ Limitations

* Different banks and payment providers use different SMS formats.
* A small training dataset can reduce classification performance for unfamiliar merchants.
* The current setup is designed as a local prototype.
* Transaction SMS messages may contain sensitive financial information.

## 🚀 Future Enhancements

* Support for more SMS formats
* Larger and more diverse training datasets
* Improved merchant recognition
* User authentication
* HTTPS and secure deployment
* Budget management
* Spending alerts
* Advanced analytics
* Data export
* Cloud synchronization

## 📄 Disclaimer

This project is developed as an academic mini project and prototype. It is intended for educational and demonstration purposes. Production deployment would require stronger security, privacy controls, and broader validation.
