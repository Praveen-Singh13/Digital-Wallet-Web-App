from app.config.database import get_db_connection
from datetime import datetime

class TransactionModel:

    @staticmethod
    def add_transaction(user_id, amount, category_id, merchant, type):
        db = get_db_connection()
        query = """
            INSERT INTO transactions (user_id, amount, category_id, merchant, type, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        db.execute(query, (
            user_id,
            amount,
            category_id,
            merchant,
            type,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        db.commit()
        return True

    @staticmethod
    def edit_transaction(transaction_id, user_id, amount, category_id, merchant, type):
        db = get_db_connection()
        query = """
            UPDATE transactions
            SET amount = ?, category_id = ?, merchant = ?, type = ?
            WHERE id = ? AND user_id = ?
        """
        db.execute(query, (
            amount,
            category_id,
            merchant,
            type,
            transaction_id,
            user_id
        ))
        db.commit()
        return True

    @staticmethod
    def delete_transaction(transaction_id, user_id):
        db = get_db_connection()
        query = """
            DELETE FROM transactions
            WHERE id = ? AND user_id = ?
        """
        db.execute(query, (transaction_id, user_id))
        db.commit()
        return True

    @staticmethod
    def get_transaction_by_id(transaction_id, user_id):
        db = get_db_connection()
        query = """
            SELECT * FROM transactions
            WHERE id = ? AND user_id = ?
        """
        row = db.execute(query, (transaction_id, user_id)).fetchone()
        return dict(row) if row else None

    @staticmethod
    def get_all_transactions(user_id):
        db = get_db_connection()
        query = """
            SELECT
                t.id, t.amount, t.type, t.date,
                t.merchant,
                c.name AS category
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = ?
            ORDER BY t.date DESC
        """
        rows = db.execute(query, (user_id,)).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def filter_transactions(user_id, category_id=None, month=None, year=None, merchant=None):
        db = get_db_connection()

        query = """
            SELECT
                t.id, t.amount, t.type, t.date,
                t.merchant, c.name AS category
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = ?
        """

        params = [user_id]

        if category_id:
            query += " AND t.category_id = ?"
            params.append(category_id)

        if month:
            query += " AND strftime('%m', t.date) = ?"
            params.append(f"{month:02d}")

        if year:
            query += " AND strftime('%Y', t.date) = ?"
            params.append(str(year))

        if merchant:
            query += " AND t.merchant LIKE ?"
            params.append(f"%{merchant}%")

        query += " ORDER BY t.date DESC"

        rows = db.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def get_recent_transactions(user_id, limit=5):
        db = get_db_connection()
        query = """
            SELECT
                t.id, t.amount, t.type, t.date,
                t.merchant,
                c.name AS category
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = ?
            ORDER BY t.date DESC
            LIMIT ?
        """
        rows = db.execute(query, (user_id, limit)).fetchall()
        return [dict(r) for r in rows]
