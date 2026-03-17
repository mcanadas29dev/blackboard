import sqlite3
from flask import current_app, g


def get_pizarra_db():
    """Conexión de solo lectura a ipizarra.db"""
    if "pizarra_db" not in g:
        g.pizarra_db = sqlite3.connect(
            current_app.config["PIZARRA_DB_PATH"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.pizarra_db.row_factory = sqlite3.Row
        # Solo lectura para datos del catálogo (seguridad)
        g.pizarra_db.execute("PRAGMA query_only = ON")
    return g.pizarra_db


def get_pizarra_db_write():
    """Conexión de escritura a ipizarra.db (solo para lista_compra)"""
    if "pizarra_db_write" not in g:
        g.pizarra_db_write = sqlite3.connect(
            current_app.config["PIZARRA_DB_PATH"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.pizarra_db_write.row_factory = sqlite3.Row
    return g.pizarra_db_write


def get_users_db():
    """Conexión de lectura/escritura a users.db"""
    if "users_db" not in g:
        g.users_db = sqlite3.connect(
            current_app.config["USERS_DB_PATH"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.users_db.row_factory = sqlite3.Row
    return g.users_db


def close_db(e=None):
    """Cierra todas las conexiones al final del request"""
    for key in ("pizarra_db", "pizarra_db_write", "users_db"):
        db = g.pop(key, None)
        if db is not None:
            db.close()


def init_users_db(app):
    """Crea la tabla users si no existe (solo en users.db)"""
    with app.app_context():
        db = sqlite3.connect(app.config["USERS_DB_PATH"])
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                username  TEXT    NOT NULL UNIQUE,
                password  TEXT    NOT NULL,
                activo    BOOLEAN NOT NULL DEFAULT 1,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        db.commit()
        db.close()
