import boto3
from botocore.exceptions import NoCredentialsError
from storage_manager import BookStorage


class S3Storage(BookStorage):
    def __init__(self, bucket_name, region_name="us-east-1", folder_name="downloads", word_count_folder="processed"):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3", region_name=region_name)
        self.folder_name = folder_name.rstrip('/')
        self.word_count_folder = word_count_folder
        self.word_count_file = f"{self.word_count_folder}/word_counts.txt"


    def upload_book(self, book_id, content, count):
        key = f"{self.folder_name}/pg{count}.txt"
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=content,
                ContentType="text/plain"
            )
        except NoCredentialsError:
            print("AWS credentials not found. Check your configuration.")
        except Exception as e:
            print(f"Error uploading book pg{book_id} to S3: {e}")

    def delete_all_books(self):
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=f"{self.folder_name}/"
            )

            if 'Contents' in response:
                objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]

                self.s3_client.delete_objects(
                    Bucket=self.bucket_name,
                    Delete={
                        'Objects': objects_to_delete,
                        'Quiet': True
                    }
                )
            else:
                print(f"No books found in the folder {self.folder_name}.")
        except NoCredentialsError:
            print("AWS credentials not found. Check your configuration.")
        except Exception as e:
            print(f"Error deleting books from the folder {self.folder_name}: {e}")

    def upload_word_counts(self, word_counter):
        try:
            word_count_str = "\n".join([f"{word} {count}" for word, count in word_counter.items()])
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=self.word_count_file,
                Body=word_count_str,
                ContentType="text/plain"
            )
        except NoCredentialsError:
            print("AWS credentials not found. Check your configuration.")
        except Exception as e:
            print(f"Error uploading word counts to S3: {e}")

    def delete_output_file(self):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=self.word_count_file)
        except NoCredentialsError:
            print("AWS credentials not found. Check your configuration.")
        except Exception as e:
            print(f"Error deleting the file {self.word_count_file} from S3: {e}")