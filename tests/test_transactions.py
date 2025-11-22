import pytest
from app import create_app
from app.config.database import get_db


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        with app.app_context():
            db = get_db()

            db.executescript("""
                DELETE FROM users;
                DELETE FROM wallet;
                DELETE FROM categories;
                DELETE FROM transactions;

                INSERT INTO users (id, name, email, password)
                VALUES (1, 'Transaction Tester', 'txn@test.com', 'hashed');

                INSERT INTO wallet (user_id, balance)
                VALUES (1, 1000);

                INSERT INTO categories (id, user_id, name)
                VALUES
                    (1, 1, 'Food'),
                    (2, 1, 'Travel'),
                    (3, 1, 'Bills');

                INSERT INTO transactions (id, user_id, type, amount, category_id, merchant, date)
                VALUES
                    (1, 1, 'expense', 200, 1, 'KFC', '2025-01-10'),
                    (2, 1, 'income', 1500, NULL, 'Salary', '2025-01-01'),
                    (3, 1, 'expense', 300, 2, 'Uber', '2025-01-12');
            """)
            db.commit()

        yield client


def test_add_transaction(client):
    payload = {
        "type": "expense",
        "amount": 120,
        "category_id": 1,
        "merchant": "Dominos",
        "date": "2025-01-20"
    }

    response = client.post("/transactions/add", data=payload, follow_redirects=True)

    assert response.status_code == 200
    assert b"Transactions" in response.data or b"added" in response.data


def test_edit_transaction(client):
    payload = {
        "type": "expense",
        "amount": 250,
        "category_id": 1,
        "merchant": "Updated Store",
        "date": "2025-01-11"
    }

    response = client.post("/transactions/edit/1", data=payload, follow_redirects=True)

    assert response.status_code == 200
    assert b"Updated Store" in response.data or b"edited" in response.data


def test_delete_transaction(client):
    response = client.post("/transactions/delete/1", follow_redirects=True)

    assert response.status_code == 200
    assert b"Transactions" in response.data or b"deleted" in response.data


def test_filter_transactions_by_category(client):
    response = client.get("/transactions?category=Food")
    assert response.status_code == 200
    assert b"KFC" in response.data


def test_filter_transactions_by_month_year(client):
    response = client.get("/transactions?month=1&year=2025")
    assert response.status_code == 200
    assert b"2025" in response.data


def test_api_transactions(client):
    response = client.get("/api/transactions")
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["transactions"]) >= 3


def test_api_add_transaction(client):
    payload = {
        "type": "income",
        "amount": 777,
        "merchant": "Freelance",
        "date": "2025-01-25",
        "category_id": None
    }

    response = client.post("/api/transactions/add", json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["transaction"]["merchant"] == "Freelance"
    assert data["transaction"]["amount"] == 777


def test_api_delete_transaction(client):
    response = client.post("/api/transactions/delete/3")
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
