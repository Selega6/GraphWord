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

    @patch("crawler.gutenberg_crawler.requests.get")
    @patch("crawler.gutenberg_crawler.Gutenberg_crawler.is_english", return_value=True)
    def test_download_book_success(self, mock_is_english, mock_requests_get):
        """Prueba que download_book descarga un libro con éxito."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Sample book content"
        mock_requests_get.return_value = mock_response

        mock_storage = MagicMock()
        crawler = gutenberg_crawler.Gutenberg_crawler(book_count=1, storage=mock_storage)

        result = crawler.download_book(123, 0)  # Ahora pasamos 'count' como segundo argumento

        self.assertTrue(result)
        mock_is_english.assert_called_once_with(123)
        mock_requests_get.assert_called_once_with("https://www.gutenberg.org/cache/epub/123/pg123.txt", stream=True)
        mock_storage.upload_book.assert_called_once_with(123, b"Sample book content", 0)

    @unittest.mock.patch("crawler.gutenberg_crawler.Gutenberg_crawler.download_book", side_effect=[True, True, False, True])
    @unittest.mock.patch("crawler.gutenberg_crawler.Gutenberg_crawler.generate_random_book_id", side_effect=[1, 2, 3, 4])
    def test_download_books(self, mock_generate_random_book_id, mock_download_book):
        crawler = gutenberg_crawler.Gutenberg_crawler(book_count=3)
        crawler.download_books()
        
        self.assertEqual(mock_download_book.call_count, 4)
        self.assertEqual(mock_generate_random_book_id.call_count, 4)
