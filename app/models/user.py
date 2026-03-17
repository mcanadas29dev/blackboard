from flask_login import UserMixin
from app.database import get_users_db


class User(UserMixin):
    def __init__(self, id, username, activo):
        self.id = id
        self.username = username
        self.activo = activo

    def is_active(self):
        return bool(self.activo)

    @staticmethod
    def get_by_id(user_id):
        db = get_users_db()
        row = db.execute(
            "SELECT id, username, activo FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if row:
            return User(row["id"], row["username"], row["activo"])
        return None

    @staticmethod
    def get_by_username(username):
        db = get_users_db()
        row = db.execute(
            "SELECT id, username, password, activo FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        return row  # Devuelve la fila completa (incluye hash de password)
