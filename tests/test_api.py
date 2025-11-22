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
                DELETE FROM transactions;
                DELETE FROM categories;

                INSERT INTO users (id, name, email, password)
                VALUES (1, 'Test User', 'api@test.com', 'hashed');

                INSERT INTO wallet (user_id, balance)
                VALUES (1, 1000);

                INSERT INTO categories (id, user_id, name)
                VALUES (1, 1, 'Food'), (2, 1, 'Travel');

                INSERT INTO transactions (id, user_id, type, amount, category_id, merchant, date)
                VALUES
                    (1, 1, 'expense', 200, 1, 'Subway', '2025-01-10'),
                    (2, 1, 'income', 1500, NULL, 'Salary', '2025-01-01');
            """)
            db.commit()

        yield client


def test_api_wallet_balance(client):
    response = client.get("/api/wallet/balance")
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["balance"] == 1000


def test_api_wallet_deposit(client):
    response = client.post("/api/wallet/deposit", json={"amount": 500})
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["new_balance"] == 1500


def test_api_wallet_withdraw(client):
    response = client.post("/api/wallet/withdraw", json={"amount": 200})
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["new_balance"] == 800


def test_api_transactions_list(client):
    response = client.get("/api/transactions")
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["transactions"]) >= 2


def test_api_add_transaction(client):
    payload = {
        "type": "expense",
        "amount": 100,
        "category_id": 1,
        "merchant": "KFC",
        "date": "2025-01-20"
    }

    response = client.post("/api/transactions/add", json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["transaction"]["merchant"] == "KFC"


def test_api_analytics_summary(client):
    response = client.get("/api/analytics/summary")
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert "total_spent" in data
    assert "total_income" in data


def test_api_categories(client):
    response = client.get("/api/categories")
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["categories"]) >= 2


def test_api_profile_fetch(client):
    response = client.get("/api/profile/1")
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["profile"]["name"] == "Test User"


def test_api_profile_update(client):
    payload = {"name": "Updated User"}

    response = client.post("/api/profile/update/1", json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["profile"]["name"] == "Updated User"
