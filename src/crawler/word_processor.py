import boto3
from collections import Counter
from nltk.corpus import stopwords
import nltk

nltk.data.path.append('./nltk_data')

class WordProcessor:
    def __init__(self, input_dir, lower_bound=3, upper_bound=5, s3_bucket="graphword-bucket"):
        self.input_dir = input_dir.rstrip('/')
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.s3_bucket = s3_bucket

        self.s3_client = boto3.client("s3")

        self.stopwords = set(stopwords.words("english"))

    def process_files(self):
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.s3_bucket, Prefix=self.input_dir)

            if 'Contents' not in response:
                print(f"No se encontraron archivos en '{self.s3_bucket}/{self.input_dir}'.")
                return Counter()

            word_counter = Counter()

            for obj in response['Contents']:
                file_key = obj['Key']
                if not file_key.endswith(".txt"):
                    continue 

                content = self.s3_client.get_object(Bucket=self.s3_bucket, Key=file_key)
                file_content = content['Body'].read().decode('utf-8')

                word_counter.update(self.process_file_content(file_content))

            return word_counter

        except boto3.exceptions.Boto3Error as e:
            print(f"Error al acceder a S3: {e}")
            return Counter()
        except Exception as e:
            print(f"Error inesperado al procesar archivos de S3: {e}")
            return Counter()

    def process_file_content(self, content):
        word_counter = Counter()
        try:
            for line in content.splitlines():
                words = line.strip().split()
                filtered_words = [
                    word.lower().strip(".,!?;:\"()[]{}<>")
                    for word in words
                    if self.lower_bound <= len(word) <= self.upper_bound and word.lower() not in self.stopwords
                ]
                word_counter.update(filtered_words)
        except Exception as e:
            print(f"Error al procesar el contenido del archivo: {e}")
        return word_counter
