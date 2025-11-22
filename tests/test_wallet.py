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

                INSERT INTO users (id, name, email, password)
                VALUES (1, 'Wallet Tester', 'wallet@test.com', 'hashed');

                INSERT INTO wallet (user_id, balance)
                VALUES (1, 1000);

                INSERT INTO transactions (id, user_id, type, amount, category_id, merchant, date)
                VALUES
                    (1, 1, 'expense', 200, NULL, 'Food', '2025-01-10'),
                    (2, 1, 'income', 1500, NULL, 'Salary', '2025-01-01');
            """)
            db.commit()

        yield client


def test_get_wallet_page(client):
    response = client.get("/wallet")
    assert response.status_code == 200
    assert b"Wallet" in response.data


def test_deposit_money(client):
    response = client.post("/wallet/deposit", json={"amount": 500})
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["new_balance"] == 1500


def test_withdraw_money(client):
    response = client.post("/wallet/withdraw", json={"amount": 300})
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["new_balance"] == 700


def test_withdraw_exceed_balance(client):
    response = client.post("/wallet/withdraw", json={"amount": 20000})
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is False
    assert "insufficient" in data["message"].lower()


def test_wallet_history_loaded(client):
    response = client.get("/wallet")
    assert response.status_code == 200
    assert b"Salary" in response.data
    assert b"Food" in response.data


def test_api_wallet_balance(client):
    response = client.get("/api/wallet/balance")
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["balance"] == 1000
