import csv
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_price(raw_price: str) -> float:
    """Преобразует строку цены (например, '£19.99' или 'Â£19.99') в float."""
    cleaned = re.sub(r"[^\d.]", "", raw_price or "")
    if not cleaned:
        raise ValueError(f"Некорректное значение цены: {raw_price!r}")
    value = float(cleaned)
    if value < 0:
        raise ValueError(f"Отрицательная цена: {value}")
    return value


def parse_rating(star_tag) -> int:
    """Извлекает рейтинг от 1 до 5 из тега p.star-rating."""
    if star_tag is None:
        raise ValueError("Не найден тег рейтинга")
    for cls in star_tag.get("class", []):
        if cls in RATING_MAP:
            return RATING_MAP[cls]
    raise ValueError(f"Неизвестный класс рейтинга: {star_tag.get('class')}")


def fetch_books(url: str = BASE_URL, limit: int = 20) -> list[dict]:
    """Загружает первые limit книг с сайта и возвращает список словарей."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or "utf-8"
    except requests.exceptions.ConnectionError:
        print("Ошибка подключения к сайту. Проверьте интернет-соединение.")
        return []
    except requests.exceptions.Timeout:
        print("Превышено время ожидания ответа от сервера.")
        return []
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code if e.response is not None else "неизвестен"
        print(f"HTTP-ошибка при запросе к сайту (код {code}).")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сетевого запроса: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    product_pods = soup.select("article.product_pod")
    if not product_pods:
        print("На странице не найдены карточки книг.")
        return []

    books: list[dict] = []
    errors_count = 0

    for pod in product_pods[:limit]:
        try:
            title_link = pod.select_one("h3 a")
            price_tag = pod.select_one("p.price_color")
            star_tag = pod.select_one("p.star-rating")

            if title_link is None or not title_link.get("title"):
                raise ValueError("Отсутствует название книги")
            if price_tag is None:
                raise ValueError("Отсутствует цена книги")

            relative_url = (title_link.get("href") or "").strip()
            if not relative_url:
                raise ValueError("Отсутствует ссылка на книгу")

            title = title_link["title"].strip()
            price = parse_price(price_tag.get_text(strip=True))
            rating = parse_rating(star_tag)
            absolute_url = urljoin(url, relative_url)

            books.append(
                {
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "url": absolute_url,
                }
            )
        except (AttributeError, ValueError, TypeError) as e:
            errors_count += 1
            print(f"Предупреждение при разборе карточки книги: {e}")

    if not books and errors_count > 0:
        print("Не удалось корректно разобрать ни одну карточку книги.")
    return books


def get_books(url: str = BASE_URL, limit: int = 20) -> list[dict]:
    """Совместимость со старым именем функции."""
    return fetch_books(url=url, limit=limit)


def filter_by_price(books: list[dict], max_price: float) -> list[dict]:
    """Возвращает книги с ценой не выше max_price."""
    return [book for book in books if book["price"] <= max_price]


def filter_by_rating(books: list[dict], min_rating: int) -> list[dict]:
    """Возвращает книги с рейтингом не ниже min_rating."""
    return [book for book in books if book["rating"] >= min_rating]


def sort_by_price(books: list[dict]) -> list[dict]:
    """Сортирует книги по цене от самой дешёвой к самой дорогой."""
    return sorted(books, key=lambda x: x["price"])


def save_to_csv(books: list[dict], filename: str = "deals.csv") -> None:
    """Сохраняет книги в CSV-файл с кодировкой utf-8-sig."""
    try:
        with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(
                file, fieldnames=["title", "price", "rating", "url"]
            )
            writer.writeheader()
            for book in books:
                writer.writerow(
                    {
                        "title": book["title"],
                        "price": f"{book['price']:.2f}",
                        "rating": book["rating"],
                        "url": book["url"],
                    }
                )
        print(f"\nРезультаты сохранены в {filename}")
    except OSError as e:
        print(f"Ошибка при сохранении файла {filename}: {e}")


def main() -> None:
    print("DEAL RADAR — поиск выгодных предложений\n")
    all_books = fetch_books(BASE_URL, limit=20)
    if not all_books:
        print("Не удалось получить данные о книгах.")
        return

    max_price_limit = 20.0
    min_rating_limit = 4

    cheap_books = filter_by_price(all_books, max_price_limit)
    filtered_books = filter_by_rating(cheap_books, min_rating_limit)
    sorted_books = sort_by_price(filtered_books)

    print(f"Максимальная цена: £{max_price_limit:g}")
    print(f"Минимальный рейтинг: {min_rating_limit}/5")
    print(f"Найдено книг: {len(sorted_books)}\n")

    print(f"{'№':<3} | {'Название':<40} | {'Цена':<8} | {'Рейтинг'}")
    print("-" * 65)

    for idx, book in enumerate(sorted_books, 1):
        title_short = (
            book["title"]
            if len(book["title"]) <= 37
            else book["title"][:34] + "..."
        )
        print(
            f"{idx:<3} | {title_short:<40} | £{book['price']:<7.2f} | "
            f"{book['rating']}/5"
        )

    save_to_csv(sorted_books, "deals.csv")


if __name__ == "__main__":
    main()