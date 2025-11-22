from app.config.database import get_db_connection

class WalletModel:

    @staticmethod
    def get_balance(user_id):
        db = get_db_connection()
        query = """
            SELECT balance
            FROM wallet
            WHERE user_id = ?
        """
        row = db.execute(query, (user_id,)).fetchone()

        if row:
            return row["balance"]

        init_query = "INSERT INTO wallet (user_id, balance) VALUES (?, 0)"
        db.execute(init_query, (user_id,))
        db.commit()
        return 0

    @staticmethod
    def deposit(user_id, amount):
        db = get_db_connection()
        query = """
            UPDATE wallet
            SET balance = balance + ?
            WHERE user_id = ?
        """
        db.execute(query, (amount, user_id))
        db.commit()
        return True

    @staticmethod
    def withdraw(user_id, amount):
        db = get_db_connection()

        balance = WalletModel.get_balance(user_id)
        if balance < amount:
            return {"success": False, "message": "Insufficient balance"}

        query = """
            UPDATE wallet
            SET balance = balance - ?
            WHERE user_id = ?
        """
        db.execute(query, (amount, user_id))
        db.commit()

        return {"success": True, "message": "Withdrawal successful"}

    @staticmethod
    def set_monthly_limit(user_id, year, month, limit_amount):
        db = get_db_connection()

        query_check = """
            SELECT id
            FROM monthly_limits
            WHERE user_id = ? AND year = ? AND month = ?
        """

        row = db.execute(query_check, (user_id, year, month)).fetchone()

        if row:
            update_query = """
                UPDATE monthly_limits
                SET monthly_limit = ?
                WHERE id = ?
            """
            db.execute(update_query, (limit_amount, row["id"]))
        else:
            insert_query = """
                INSERT INTO monthly_limits (user_id, year, month, monthly_limit)
                VALUES (?, ?, ?, ?)
            """
            db.execute(insert_query, (user_id, year, month, limit_amount))

        db.commit()
        return True

    @staticmethod
    def get_monthly_limit(user_id, year, month):
        db = get_db_connection()

        query = """
            SELECT monthly_limit
            FROM monthly_limits
            WHERE user_id = ? AND year = ? AND month = ?
        """

        row = db.execute(query, (user_id, year, month)).fetchone()

        if not row:
            return None

        return row["monthly_limit"]
