import boto3
from botocore.exceptions import NoCredentialsError
from storage_manager import BookStorage


class S3Storage(BookStorage):
    def __init__(self, bucket_name, region_name="us-east-1", folder_name="downloads", word_count_file="processed/word_counts.txt"):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3", region_name=region_name)
        self.folder_name = folder_name.rstrip('/')
        self.word_count_file = word_count_file

    def upload_book(self, book_id, content):
        key = f"{self.folder_name}/pg{book_id}.txt"
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=content,
                ContentType="text/plain"
            )
        except NoCredentialsError:
            print("No se encontraron credenciales de AWS. Verifica tu configuración.")
        except Exception as e:
            print(f"Error al subir el libro pg{book_id} a S3: {e}")

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
                print(f"No se encontraron libros en la carpeta {self.folder_name}.")
        except NoCredentialsError:
            print("No se encontraron credenciales de AWS. Verifica tu configuración.")
        except Exception as e:
            print(f"Error al eliminar libros de la carpeta {self.folder_name}: {e}")

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
            print("No se encontraron credenciales de AWS. Verifica tu configuración.")
        except Exception as e:
            print(f"Error al subir el conteo de palabras a S3: {e}")

    def delete_output_file(self):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=self.word_count_file)
            print(f"Archivo {self.word_count_file} eliminado de S3 exitosamente.")
        except NoCredentialsError:
            print("No se encontraron credenciales de AWS. Verifica tu configuración.")
        except Exception as e:
            print(f"Error al eliminar el archivo {self.word_count_file} de S3: {e}")
