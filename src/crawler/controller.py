import schedule
import time
from gutenberg_crawler import Gutenberg_crawler
from word_processor import WordProcessor


class Controller:
    def __init__(self, crawler, processor):
        self.crawler = crawler
        self.processor = processor

    def schedule_downloads(self):
        schedule.every().day.at("03:00").do(self.download_and_process)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def execute(self):
        self.delete_downloads_and_output()
        self.download_and_process()

    def execute_schedule(self):
        self.schedule_downloads()

    def download_and_process(self):
        self.crawler.download_books()
        word_counter = self.processor.process_files()
        self.crawler.storage.upload_word_counts(word_counter)

    def delete_downloads_and_output(self):
        self.crawler.storage.delete_all_books()
        self.crawler.storage.delete_output_file()
