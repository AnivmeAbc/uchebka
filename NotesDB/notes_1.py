import sqlite3
from datetime import datetime

DB_NAME = "notes.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_table():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT
            )
        """)

def add_note():
    title = input("Заголовок: ")
    content = input("Текст: ")
    created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with connect() as conn:
        conn.execute("INSERT INTO notes(title, content, created_at) VALUES (?, ?, ?)",
                     (title, content, created))
        print("✅ Заметка добавлена!")

def show_notes():
    with connect() as conn:
        cur = conn.execute("SELECT id, title, created_at FROM notes ORDER BY created_at DESC")
        rows = cur.fetchall()

        if not rows:
            print("Заметок пока нет 😔")
            return

        for row in rows:
            print(f"[{row[0]}] {row[1]} ({row[2]})")

def view_note():
    note_id = input("ID заметки: ")
    with connect() as conn:
        cur = conn.execute("SELECT * FROM notes WHERE id=?", (note_id,))
        note = cur.fetchone()

        if note:
            print("\nЗАГОЛОВОК:", note[1])
            print("ТЕКСТ:", note[2])
            print("СОЗДАНО:", note[3])
            print("ОБНОВЛЕНО:", note[4])
        else:
            print("❌ Заметка не найдена")

def update_note():
    note_id = input("ID для редактирования: ")
    new_text = input("Новый текст: ")
    updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with connect() as conn:
        cur = conn.execute("UPDATE notes SET content=?, updated_at=? WHERE id=?",
                           (new_text, updated, note_id))

        if cur.rowcount:
            print("✏️ Обновлено")
        else:
            print("❌ Заметка не найдена")

def delete_note():
    note_id = input("ID для удаления: ")
    with connect() as conn:
        cur = conn.execute("DELETE FROM notes WHERE id=?", (note_id,))

        if cur.rowcount:
            print("🗑 Удалено")
        else:
            print("❌ Заметка не найдена")

def search_notes():
    word = input("Ключевое слово: ")
    with connect() as conn:
        cur = conn.execute("SELECT id, title FROM notes WHERE title LIKE ? OR content LIKE ?",
                           (f"%{word}%", f"%{word}%"))
        results = cur.fetchall()

        for note in results:
            print(f"[{note[0]}] {note[1]}")
        if not results:
            print("Ничего не найдено 😴")

def menu():
    print("""
1 — Добавить заметку
2 — Показать все
3 — Просмотреть
4 — Редактировать
5 — Удалить
6 — Поиск
0 — Выход
""")

def main():
    create_table()
    while True:
        menu()
        choice = input("Выбор: ")

        if choice == "1":
            add_note()
        elif choice == "2":
            show_notes()
        elif choice == "3":
            view_note()
        elif choice == "4":
            update_note()
        elif choice == "5":
            delete_note()
        elif choice == "6":
            search_notes()
        elif choice == "0":
            break
        else:
            print("Неверный ввод 😅")

if __name__ == "__main__":
    main()
