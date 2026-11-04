import sqlite3
from datetime import datetime

DB_NAME = "capsules.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS capsules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            author TEXT NOT NULL,
            open_date TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def create_capsule(title, message, author, open_date):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO capsules (title, message, author, open_date, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (title, message, author, open_date, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_capsules():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM capsules ORDER BY open_date").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_capsule(capsule_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM capsules WHERE id = ?", (capsule_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def delete_capsule(capsule_id):
    conn = get_connection()
    cursor = conn.execute("DELETE FROM capsules WHERE id = ?", (capsule_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted