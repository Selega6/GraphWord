import os
import json
from gutenberg_crawler import Gutenberg_crawler
from word_processor import WordProcessor
from s3_storage_manager import S3Storage
from controller import Controller

def lambda_handler(event, context):
    bucket_name = os.getenv("BUCKET_NAME", "tu-bucket-s3")
    download_folder = os.getenv("DOWNLOAD_FOLDER", "downloads")
    output_file = os.getenv("OUTPUT_FILE", "processed/word_counts.txt")

    try:
        s3_storage = S3Storage(bucket_name, folder_name=download_folder)

        book_count = 20
        crawler = Gutenberg_crawler(book_count, s3_storage)
        processor = WordProcessor(
            bucket_name=bucket_name,
            input_folder=download_folder,
            output_file=output_file,
            lower_bound=3,
            upper_bound=5
        )

        controller = Controller(crawler, processor)

        controller.execute()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Proceso completado exitosamente",
                "output_file": output_file
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Error durante el procesamiento",
                "error": str(e)
            })
        }
