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

                INSERT INTO users (id, name, email, password)
                VALUES (1, 'Test User', 'test@auth.com', 'hashedpassword');

                INSERT INTO wallet (user_id, balance)
                VALUES (1, 0);
            """)
            db.commit()

        yield client


def test_signup(client):
    payload = {
        "name": "New User",
        "email": "newuser@example.com",
        "password": "password1"
    }

    response = client.post("/signup", data=payload, follow_redirects=True)

    assert response.status_code == 200
    assert b"Login" in response.data or b"Dashboard" in response.data


def test_login_success(client):
    payload = {
        "email": "test@auth.com",
        "password": "hashedpassword"
    }

    response = client.post("/login", data=payload, follow_redirects=True)

    assert response.status_code == 200
    assert b"Dashboard" in response.data


def test_login_failure(client):
    payload = {
        "email": "test@auth.com",
        "password": "wrongpass"
    }

    response = client.post("/login", data=payload, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid" in response.data or b"incorrect" in response.data


def test_logout(client):

    client.post("/login", data={
        "email": "test@auth.com",
        "password": "hashedpassword"
    })

    response = client.get("/logout", follow_redirects=True)

    assert response.status_code == 200
    assert b"Login" in response.data or b"Welcome back" in response.data
