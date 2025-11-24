import sqlite3

DB_NAME = "notes.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

def add_note(title: str, content: str):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        conn.commit()

def get_notes():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, content, created_at FROM notes")
        return cur.fetchall()

def delete_note(note_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()