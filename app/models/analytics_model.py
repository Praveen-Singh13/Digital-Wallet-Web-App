from app.config.database import get_db_connection
from datetime import datetime

class AnalyticsModel:

    @staticmethod
    def get_monthly_summary(user_id, year, month):
        db = get_db_connection()
        query = """
            SELECT
                SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) AS total_spent,
                SUM(CASE WHEN type='income' THEN amount ELSE 0 END) AS total_income,
                COUNT(*) AS transaction_count
            FROM transactions
            WHERE user_id = ?
            AND strftime('%Y', date) = ?
            AND strftime('%m', date) = ?
        """
        row = db.execute(query, (user_id, str(year), f"{month:02d}")).fetchone()
        return dict(row) if row else {}

    @staticmethod
    def get_category_distribution(user_id, year, month):
        db = get_db_connection()
        query = """
            SELECT
                c.name AS category,
                SUM(t.amount) AS total
            FROM transactions t
            JOIN categories c ON c.id = t.category_id
            WHERE t.user_id = ?
            AND t.type = 'expense'
            AND strftime('%Y', t.date) = ?
            AND strftime('%m', t.date) = ?
            GROUP BY t.category_id
            ORDER BY total DESC
        """
        rows = db.execute(query, (user_id, str(year), f"{month:02d}")).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def get_yearly_totals(user_id, year):
        db = get_db_connection()
        query = """
            SELECT
                strftime('%m', date) AS month,
                SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) AS expenses,
                SUM(CASE WHEN type='income' THEN amount ELSE 0 END) AS income
            FROM transactions
            WHERE user_id = ?
            AND strftime('%Y', date) = ?
            GROUP BY strftime('%m', date)
            ORDER BY month
        """
        rows = db.execute(query, (user_id, str(year))).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def detect_overspending(user_id, year, month):
        db = get_db_connection()

        limit_query = """
            SELECT monthly_limit
            FROM monthly_limits
            WHERE user_id = ?
            AND year = ?
            AND month = ?
        """

        row = db.execute(limit_query, (user_id, year, month)).fetchone()
        if not row:
            return {"limit_set": False, "limit": 0, "spent": 0, "exceeded": False}

        monthly_limit = row["monthly_limit"]

        spent_query = """
            SELECT SUM(amount) AS spent
            FROM transactions
            WHERE user_id = ?
            AND type = 'expense'
            AND strftime('%Y', date) = ?
            AND strftime('%m', date) = ?
        """
        spent_row = db.execute(spent_query, (user_id, str(year), f"{month:02d}")).fetchone()
        spent = spent_row["spent"] or 0

        exceeded = spent > monthly_limit

        return {
            "limit_set": True,
            "limit": monthly_limit,
            "spent": spent,
            "exceeded": exceeded
        }
