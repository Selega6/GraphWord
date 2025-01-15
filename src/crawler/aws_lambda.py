import os
import json
import boto3
from gutenberg_crawler import Gutenberg_crawler
from word_processor import WordProcessor
from s3_storage_manager import S3Storage
from controller import Controller

def lambda_handler(event, context):
    bucket_name = os.getenv("BUCKET_NAME", "graphword-bucket")
    download_folder = "downloads"
    output_file = os.getenv("OUTPUT_FILE", "processed/word_counts.txt")
    queue_url = os.getenv("QUEUE_URL")

    sqs = boto3.client('sqs')

    try:
        s3_storage = S3Storage(bucket_name, folder_name=download_folder)

        book_count = 20
        crawler = Gutenberg_crawler(book_count, s3_storage)
        processor = WordProcessor(
            s3_bucket=bucket_name,
            input_dir=download_folder,
            lower_bound=3,
            upper_bound=5
        )

        controller = Controller(crawler, processor)

        controller.execute()

        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({
                "status": "completed",
                "output_file": output_file
            })
        )

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
