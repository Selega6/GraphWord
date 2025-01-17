from gutenberg_crawler import Gutenberg_crawler  
from controller import Controller
from word_processor import WordProcessor
from s3_storage_manager import S3Storage

def main():
    input_dir = "downloads"
    word_count_folder = "processed"
    lower_bound = 3
    upper_bound = 5

    storage = S3Storage(
        folder_name="downloads", 
        bucket_name="graphword-bucket", 
        word_count_folder=word_count_folder
    )

    processor = WordProcessor(input_dir, lower_bound, upper_bound)
    crawler = Gutenberg_crawler(20, storage)

    controller = Controller(crawler, processor)
    controller.execute()

if __name__ == "__main__":
    main()
