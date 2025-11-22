Digital Wallet & Expense Tracker
===============================

A modern, feature-rich wallet application built with Flask, SQLite, Jinja, and Chart.js. It provides secure authentication, real-time wallet management, detailed analytics, and a clean glass‑morphism UI.

Project Features
----------------

Wallet Management
-----------------
- Real-time balance display
- Deposit and withdrawal functionality
- Monthly spending limit
- Overspending alerts

Transactions
------------
- Add, edit, delete transactions
- Automatic wallet update after each transaction
- Category support (Food, Travel, Bills, etc.)
- Advanced filtering: Category, Month, Year, Merchant
- AJAX-based updates without page reloads

Analytics Dashboard
-------------------
- Monthly summary metrics
- Category-wise spending chart
- Yearly income vs expense graph
- Overspending detection

Authentication
--------------
- Signup, Login, Logout
- Password hashing
- Session-based authentication
- User-specific data isolation

Tech Stack
----------
Backend: Flask, Jinja2, SQLite
Frontend: HTML, CSS, JavaScript
Charts: Chart.js
Async: AJAX (Fetch API)

## Project Structure

```
wallet/
│── app/
│   │── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user_model.py
│   │   ├── wallet_model.py
│   │   ├── transaction_model.py
│   │   ├── category_model.py
│   │   └── analytics_model.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   ├── wallet_routes.py
│   │   ├── transaction_routes.py
│   │   ├── analytics_routes.py
│   │   ├── profile_routes.py
│   │   └── api_routes.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       ├── formatters.py
│       └── alerts.py
│
│── database/
│   ├── wallet.db
│   ├── schema.sql
│   └── seed_data.sql
│
│── templates/
│   ├── layout.html
│   ├── navbar.html
│   ├── sidebar.html
│   ├── footer.html
│   ├── dashboard.html
│   ├── transactions.html
│   ├── transaction_add.html
│   ├── analytics.html
│   ├── profile.html
│   ├── login.html
│   └── signup.html
│
│── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── dashboard.css
│   │   ├── transactions.css
│   │   ├── analytics.css
│   │   ├── auth.css
│   │   └── wallet.css
│   │
│   ├── js/
│   │   ├── main.js
│   │   ├── dashboard.js
│   │   ├── transactions.js
│   │   ├── analytics.js
│   │   ├── profile.js
│   │   └── wallet.js
│   │
│   └── img/
│       └── logos, icons...
│
│── tests/
│   ├── test_auth.py
│   ├── test_wallet.py
│   ├── test_transactions.py
│   ├── test_analytics.py
│   └── test_api.py
│
│── run.py
│── README.md
│── requirements.txt
```


Installation & Setup
--------------------

1. Clone the repository
   git clone <repo_url>
   cd wallet

2. Create a virtual environment
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

4. Initialize the database
   python3 - << 'EOF'
   from app.config.database import init_db_if_needed
   init_db_if_needed()
   print("Database initialized.")
   EOF

5. Run the server
   flask run

6. Open in browser
   http://127.0.0.1:5000

Security
--------
- Hashed passwords
- Session authentication
- Input validation on all operations
- User-specific data isolation

Future Enhancements
-------------------
- PDF export of reports
- Bank sync simulation
- Light/Dark mode toggle
- PWA support
- Spending suggestion engine

