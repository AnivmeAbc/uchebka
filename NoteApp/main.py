import argparse
import sqlite3
from database import init_db, add_note, get_notes, delete_note

def main():
    parser = argparse.ArgumentParser(description="NoteApp — приложение для заметок")
    parser.add_argument("action", choices=["init", "add", "list", "delete"])
    parser.add_argument("--title", help="Заголовок заметки")
    parser.add_argument("--content", help="Текст заметки")
    parser.add_argument("--id", type=int, help="ID заметки для удаления")
    args = parser.parse_args()

    try:
        if args.action == "init":
            init_db()
            print("База данных создана или уже существует.")

        elif args.action == "add":
            if not args.title or not args.content:
                print("Ошибка: Для добавления нужно передать --title и --content")
                return
            add_note(args.title, args.content)
            print("Заметка добавлена.")

        elif args.action == "list":
            try:
                notes = get_notes()
                if not notes:
                    print("Заметок нет.")
                for n in notes:
                    # n[0]=id, n[1]=title, n[2]=content, n[3]=date
                    print(f"[{n[0]}] {n[1]} — {n[3]}\n{n[2]}\n")
            except sqlite3.OperationalError:
                print("Ошибка: База данных не найдена. Сначала выполните 'init'.")

        elif args.action == "delete":
            if args.id is None:
                print("Ошибка: Для удаления нужно передать --id")
                return
            delete_note(args.id)
            print(f"Заметка с ID {args.id} удалена (если существовала).")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()