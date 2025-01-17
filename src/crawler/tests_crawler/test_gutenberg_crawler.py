import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import MagicMock, patch, mock_open
from crawler import gutenberg_crawler


class TestGutenbergCrawler(unittest.TestCase):

    def test_generate_random_book_id(self):
        crawler = gutenberg_crawler.Gutenberg_crawler()
        for _ in range(100):
            book_id = crawler.generate_random_book_id()
            self.assertGreaterEqual(book_id, crawler.BOOK_ID_RANGE[0])
            self.assertLessEqual(book_id, crawler.BOOK_ID_RANGE[1])

    @unittest.mock.patch("requests.get")
    def test_is_english_true(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.text = """
            <html>
            <th>Language</th>
            <td>English</td>
            </html>
        """
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        crawler = gutenberg_crawler.Gutenberg_crawler()
        self.assertTrue(crawler.is_english(123))
        mock_get.assert_called_once_with(f"{crawler.METADATA_URL}123")

    @unittest.mock.patch("requests.get")
    @unittest.mock.patch("crawler.gutenberg_crawler.Gutenberg_crawler.is_english", return_value=True)
    def test_download_book_success(self, mock_is_english, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.content = "Libro en inglés"
        mock_get.return_value = mock_response

        storage_mock = unittest.mock.Mock()
        crawler = gutenberg_crawler.Gutenberg_crawler(storage=storage_mock)
        result = crawler.download_book(123)

        self.assertTrue(result)
        mock_get.assert_called_once_with(f"{crawler.BASE_URL}123/pg123.txt", stream=True)
        storage_mock.upload_book.assert_called_once_with(123, "Libro en inglés")

    @unittest.mock.patch("crawler.gutenberg_crawler.Gutenberg_crawler.download_book", side_effect=[True, True, False, True])
    @unittest.mock.patch("crawler.gutenberg_crawler.Gutenberg_crawler.generate_random_book_id", side_effect=[1, 2, 3, 4])
    def test_download_books(self, mock_generate_random_book_id, mock_download_book):
        crawler = gutenberg_crawler.Gutenberg_crawler(book_count=3)
        crawler.download_books()
        
        self.assertEqual(mock_download_book.call_count, 4)
        self.assertEqual(mock_generate_random_book_id.call_count, 4)

if __name__ == "__main__":
    unittest.main()
