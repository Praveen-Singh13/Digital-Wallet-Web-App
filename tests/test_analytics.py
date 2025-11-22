import json
import pytest
from app import create_app
from app.config.database import get_db


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def db():
    conn = get_db()
    yield conn
    conn.close()


def seed_transactions(db):
    cursor = db.cursor()
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM wallet")

    cursor.execute("""
        INSERT INTO wallet(user_id, balance)
        VALUES (1, 10000)
    """)

    sample_txns = [
        (1, "expense", 500, "Food", "Swiggy", "2025-01-10"),
        (1, "expense", 2000, "Shopping", "Amazon", "2025-01-12"),
        (1, "income", 3000, "Salary", "Company", "2025-01-01"),
        (1, "expense", 800, "Travel", "Uber", "2025-01-15"),
    ]

    cursor.executemany("""
        INSERT INTO transactions (user_id, type, amount, category, merchant, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, sample_txns)

    db.commit()


def test_analytics_overview(client, db):
    seed_transactions(db)

    response = client.get("/analytics/json")
    assert response.status_code == 200

    data = json.loads(response.data)

    assert data["success"] is True
    assert "total_spent" in data
    assert "total_income" in data
    assert "category_breakdown" in data


def test_monthly_summary(client, db):
    seed_transactions(db)

    response = client.get("/analytics/monthly?year=2025")
    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert len(data["months"]) == 12
    assert data["months"][0] >= 0


def test_category_distribution(client, db):
    seed_transactions(db)

    response = client.get("/analytics/categories")
    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert isinstance(data["categories"], list)
    assert any(c["category"] == "Food" for c in data["categories"])


def test_overspending_alert(client, db):
    seed_transactions(db)

    cursor = db.cursor()
    cursor.execute("DELETE FROM monthly_limits")
    cursor.execute("""
        INSERT INTO monthly_limits (user_id, category, limit_amount)
        VALUES (1, 'Food', 400)
    """)
    db.commit()

    response = client.get("/analytics/alerts")
    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert any("exceeded" in alert["message"].lower() for alert in data["alerts"])
