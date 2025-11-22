from app.config.database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:

    @staticmethod
    def create_user(name, email, password):
        db = get_db_connection()

        check_query = "SELECT id FROM users WHERE email = ?"
        exists = db.execute(check_query, (email,)).fetchone()
        if exists:
            return {"created": False, "message": "Email already registered"}

        hashed_password = generate_password_hash(password)

        insert_query = """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
        """

        db.execute(insert_query, (name, email, hashed_password))
        db.commit()

        return {"created": True, "message": "User registered successfully"}

    @staticmethod
    def validate_login(email, password):
        db = get_db_connection()

        query = "SELECT * FROM users WHERE email = ?"
        row = db.execute(query, (email,)).fetchone()

        if row and check_password_hash(row["password"], password):
            return dict(row)

        return None

    @staticmethod
    def get_user_by_id(user_id):
        db = get_db_connection()
        query = "SELECT id, name, email FROM users WHERE id = ?"
        row = db.execute(query, (user_id,)).fetchone()
        return dict(row) if row else None

    @staticmethod
    def update_profile(user_id, name, email):
        db = get_db_connection()

        query = """
            UPDATE users
            SET name = ?, email = ?
            WHERE id = ?
        """
        db.execute(query, (name, email, user_id))
        db.commit()
        return True

    @staticmethod
    def change_password(user_id, new_password):
        db = get_db_connection()

        hashed = generate_password_hash(new_password)

        query = """
            UPDATE users
            SET password = ?
            WHERE id = ?
        """

        db.execute(query, (hashed, user_id))
        db.commit()
        return True
