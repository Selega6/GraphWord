import boto3
from botocore.exceptions import NoCredentialsError
from storage_manager import BookStorage  # Asegúrate de que esta ruta sea correcta

class s3_storage(BookStorage):
    def __init__(self, bucket_name, region_name="us-east-1", folder_name="books", word_count_file="word_counts.txt"):   
        """
        Inicializa la conexión al bucket de S3.
        :param bucket_name: Nombre del bucket S3 donde se guardarán los libros.
        :param region_name: Región de AWS donde está el bucket.
        :param folder_name: Carpeta en el bucket donde se guardarán los libros.
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3", region_name=region_name)
        self.folder_name = folder_name.rstrip('/')  # Asegura que no haya una barra al final
        self.word_count_file = word_count_file

    def upload_book(self, book_id, content):
        """
        Sube un libro a S3 con el contenido proporcionado.
        :param book_id: ID del libro (usado como nombre del archivo).
        :param content: Contenido del libro en formato de bytes.
        """
        key = f"{self.folder_name}/pg{book_id}.txt"  # Clave del archivo con prefijo de carpeta
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=content,
                ContentType="text/plain"
            )
            print(f"Libro pg{book_id} subido a S3 exitosamente en {key}.")
        except NoCredentialsError:
            print("No se encontraron credenciales de AWS. Verifica tu configuración.")
        except Exception as e:
            print(f"Error al subir el libro pg{book_id} a S3: {e}")

    def delete_all_books(self):
        """
        Elimina todos los libros de la carpeta especificada en el bucket S3.
        """
        try:
            # Listar todos los objetos en la carpeta
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=f"{self.folder_name}/"
            )

            if 'Contents' in response:
                # Crear lista de objetos para eliminar
                objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]

                # Eliminar los objetos
                delete_response = self.s3_client.delete_objects(
                    Bucket=self.bucket_name,
                    Delete={
                        'Objects': objects_to_delete,
                        'Quiet': True
                    }
                )
        except NoCredentialsError:
            print("No se encontraron credenciales de AWS. Verifica tu configuración.")
        except Exception as e:
            print(f"Error al eliminar libros de la carpeta {self.folder_name}: {e}")

    def upload_word_counts(self, word_counter):
        """
        Guarda el conteo de palabras en un archivo .txt en S3.
        :param word_counter: Contador de palabras (diccionario de palabra: frecuencia).
        """
        key = self.word_count_file
        try:
            # Crear el contenido del archivo de conteo de palabras
            word_count_str = "\n".join([f"{word} {count}" for word, count in word_counter.items()])
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=word_count_str,
                ContentType="text/plain"
            )
        except NoCredentialsError:
            print("No se encontraron credenciales de AWS. Verifica tu configuración.")
        except Exception as e:
            print(f"Error al subir el conteo de palabras a S3: {e}")

    def delete_output_file(self):
        """
        Elimina el archivo de conteo de palabras del bucket S3.
        """
        key = self.word_count_file
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
        except NoCredentialsError:
            print("No se encontraron credenciales de AWS. Verifica tu configuración.")
        except Exception as e:
            print(f"Error al eliminar el archivo de conteo de palabras de S3: {e}")