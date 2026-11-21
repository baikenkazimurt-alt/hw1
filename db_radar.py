import shutil
import sqlite3

from main import BASE_URL, fetch_books


DB_PATH = "deals.db"
BACKUP_PATH = "deals_backup.db"


def init_db(db_path: str = DB_PATH) -> None:
    """Создаёт таблицу deals с уникальным полем url."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS deals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL NOT NULL,
                rating INTEGER NOT NULL,
                url TEXT NOT NULL UNIQUE
            )
            """
        )
        conn.commit()


def save_deals_to_db(deals: list[dict], db_path: str = DB_PATH) -> None:
    """Вставляет записи через параметры (?) без повторов по url."""
    init_db(db_path)
    sql = """
        INSERT OR IGNORE INTO deals (title, price, rating, url)
        VALUES (?, ?, ?, ?)
    """
    rows = [
        (
            str(item["title"]),
            float(item["price"]),
            int(item["rating"]),
            str(item["url"]),
        )
        for item in deals
    ]
    with sqlite3.connect(db_path) as conn:
        conn.executemany(sql, rows)
        conn.commit()


def backup_db(src_path: str = DB_PATH, dst_path: str = BACKUP_PATH) -> None:
    """Создаёт резервную копию базы данных."""
    shutil.copy2(src_path, dst_path)


def run_sample_queries(db_path: str = DB_PATH) -> None:
    """Проверяет запросы с параметрами (?) вместо f-строк."""
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM deals")
        total = cur.fetchone()[0]
        print(f"Всего записей в deals.db: {total}")

        max_price = 20.0
        cur.execute(
            "SELECT title, price, rating FROM deals WHERE price <= ? ORDER BY price ASC",
            (max_price,),
        )
        cheap = cur.fetchall()
        print(f"Книг до £{max_price:g}: {len(cheap)}")

        min_rating = 4
        cur.execute(
            "SELECT title, price, rating FROM deals WHERE rating >= ? ORDER BY rating DESC, price ASC",
            (min_rating,),
        )
        top_rated = cur.fetchall()
        print(f"Книг с рейтингом >= {min_rating}: {len(top_rated)}")

        pattern = "%a%"
        cur.execute(
            "SELECT title, price FROM deals WHERE title LIKE ? ORDER BY price ASC",
            (pattern,),
        )
        matched = cur.fetchall()
        print(f"Совпадений по маске '{pattern}': {len(matched)}")


def main() -> None:
    print("Сбор данных для deals.db...")
    books = fetch_books(BASE_URL, limit=20)
    if len(books) < 10:
        print(f"Внимание: получено только {len(books)} книг (нужно минимум 10).")
        return

    save_deals_to_db(books, DB_PATH)
    # Повторный запуск проверит, что дубли по url не добавляются
    save_deals_to_db(books, DB_PATH)
    backup_db(DB_PATH, BACKUP_PATH)
    print(f"База сохранена в {DB_PATH}, резервная копия — в {BACKUP_PATH}")
    run_sample_queries(DB_PATH)


if __name__ == "__main__":
    main()