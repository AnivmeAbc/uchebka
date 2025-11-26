import sqlite3
from datetime import datetime

DB_NAME = "notes_stats.db"

def connect():
    return sqlite3.connect(DB_NAME)

def setup():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                created_at TEXT
            )
        """)

def add_note():
    title = input("Заголовок: ")
    content = input("Текст: ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with connect() as conn:
        conn.execute("INSERT INTO notes VALUES (NULL,?,?,?)",
                     (title, content, date))
        print("✅ Добавлено")

def statistics():
    with connect() as conn:
        total = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        avg_len = conn.execute("SELECT AVG(LENGTH(content)) FROM notes").fetchone()[0]
        by_day = conn.execute("""
            SELECT substr(created_at,1,10), COUNT(*) 
            FROM notes GROUP BY substr(created_at,1,10)
        """).fetchall()

    print("\n📊 СТАТИСТИКА")
    print("Всего заметок:", total)
    print("Средняя длина:", round(avg_len or 0, 2))
    print("\nПо дням:")
    for d in by_day:
        print(f"{d[0]} — {d[1]}")

def menu():
    print("""
1 — Добавить заметку
2 — Статистика
0 — Выход
""")

def main():
    setup()
    while True:
        menu()
        choice = input("Выбор: ")

        if choice == "1":
            add_note()
        elif choice == "2":
            statistics()
        elif choice == "0":
            break

if __name__ == "__main__":
    main()
