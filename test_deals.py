import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

import main as deals_main
from main import filter_by_price, filter_by_rating, parse_price, parse_rating


class BoundaryTests(unittest.TestCase):
    def test_parse_price_invalid_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_price("")
        with self.assertRaises(ValueError):
            parse_price("no price here")

    def test_parse_rating_unknown_class_raises(self) -> None:
        tag = BeautifulSoup('<p class="star-rating Zero"></p>', "html.parser").p
        with self.assertRaises(ValueError):
            parse_rating(tag)

    def test_filter_exact_boundaries(self) -> None:
        books = [
            {"title": "Exact 20", "price": 20.0, "rating": 4, "url": "https://example.com/1"},
            {"title": "Over 20", "price": 20.01, "rating": 3, "url": "https://example.com/2"},
        ]
        cheap = filter_by_price(books, 20.0)
        high_rated = filter_by_rating(books, 4)

        self.assertEqual([b["title"] for b in cheap], ["Exact 20"])
        self.assertEqual([b["title"] for b in high_rated], ["Exact 20"])


class FakeNetworkTests(unittest.TestCase):
    def test_fetch_books_with_fake_html(self) -> None:
        fake_html = """
        <html><body>
          <article class="product_pod">
            <p class="star-rating Four"></p>
            <p class="price_color">£15.50</p>
            <h3><a href="catalogue/fake-book_1/index.html" title="Fake Book">Fake Book</a></h3>
          </article>
        </body></html>
        """

        class FakeResponse:
            text = fake_html
            apparent_encoding = "utf-8"
            encoding = "utf-8"

            def raise_for_status(self) -> None:
                return None

        with patch.object(deals_main.requests, "get", return_value=FakeResponse()):
            result = deals_main.fetch_books("https://books.toscrape.com/", limit=5)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Fake Book")
        self.assertEqual(result[0]["price"], 15.5)
        self.assertEqual(result[0]["rating"], 4)
        self.assertEqual(result[0]["url"], "https://books.toscrape.com/catalogue/fake-book_1/index.html")


if __name__ == "__main__":
    unittest.main()