#!/usr/bin/env python3
"""
Herramienta CLI para gestionar usuarios de la app Pizarra.

Uso:
    python manage_users.py add <username> <password>
    python manage_users.py list
    python manage_users.py deactivate <username>
"""
import sys
import sqlite3
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

load_dotenv()
USERS_DB = os.environ.get("USERS_DB_PATH", "data/users.db")


def get_db():
    db = sqlite3.connect(USERS_DB)
    db.row_factory = sqlite3.Row
    return db


def add_user(username, password):
    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password)),
        )
        db.commit()
        print(f"✅ Usuario '{username}' creado correctamente.")
    except sqlite3.IntegrityError:
        print(f"❌ El usuario '{username}' ya existe.")
    finally:
        db.close()


def list_users():
    db = get_db()
    rows = db.execute("SELECT id, username, activo, creado_en FROM users").fetchall()
    if not rows:
        print("No hay usuarios registrados.")
    for r in rows:
        estado = "✅ activo" if r["activo"] else "🚫 inactivo"
        print(f"  [{r['id']}] {r['username']} — {estado} — creado: {r['creado_en']}")
    db.close()


def deactivate_user(username):
    db = get_db()
    db.execute("UPDATE users SET activo = 0 WHERE username = ?", (username,))
    db.commit()
    print(f"🚫 Usuario '{username}' desactivado.")
    db.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    cmd = args[0]
    if cmd == "add" and len(args) == 3:
        add_user(args[1], args[2])
    elif cmd == "list":
        list_users()
    elif cmd == "deactivate" and len(args) == 2:
        deactivate_user(args[1])
    else:
        print(__doc__)
        sys.exit(1)
