from gutenberg_crawler import Gutenberg_crawler  
from controller import Controller
from word_processor import WordProcessor
from local_storage_manager import LocalBookStorage
from s3_storage_manager import s3_storage

def main():
    input_dir = "./downloads"
    output_file = "./word_counts.txt"
    lower_bound = 3
    upper_bound = 5
    storage = LocalBookStorage()
    storage = s3_storage(folder_name = "downloads", )
    processor = WordProcessor(input_dir, output_file, lower_bound, upper_bound)
    crawler = Gutenberg_crawler(20, storage)
    controller = Controller(crawler, processor)
    controller.execute()


if __name__ == "__main__":
    main()
