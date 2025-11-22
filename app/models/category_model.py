from app.config.database import get_db_connection

class CategoryModel:

    @staticmethod
    def get_all_categories(user_id):
        db = get_db_connection()
        query = """
            SELECT id, name, type
            FROM categories
            WHERE user_id = ? OR user_id IS NULL
            ORDER BY name
        """
        rows = db.execute(query, (user_id,)).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def add_category(user_id, name, type):
        db = get_db_connection()
        query = """
            INSERT INTO categories (name, type, user_id)
            VALUES (?, ?, ?)
        """
        db.execute(query, (name, type, user_id))
        db.commit()
        return True

    @staticmethod
    def update_category(category_id, user_id, name, type):
        db = get_db_connection()
        query = """
            UPDATE categories
            SET name = ?, type = ?
            WHERE id = ? AND user_id = ?
        """
        db.execute(query, (name, type, category_id, user_id))
        db.commit()
        return True

    @staticmethod
    def delete_category(category_id, user_id):
        db = get_db_connection()
        query = """
            DELETE FROM categories
            WHERE id = ? AND user_id = ?
        """
        db.execute(query, (category_id, user_id))
        db.commit()
        return True

    @staticmethod
    def get_category_by_id(category_id):
        db = get_db_connection()
        query = "SELECT * FROM categories WHERE id = ?"
        row = db.execute(query, (category_id,)).fetchone()
        return dict(row) if row else None
