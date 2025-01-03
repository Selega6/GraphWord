import boto3

class DataLoader:
    def __init__(self, file_path=None, s3_bucket=None, s3_key=None):
        self.file_path = file_path
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.words_with_counts = None

        if file_path:
            self.words_with_counts = self.load_words()
        elif s3_bucket and s3_key:
            self.file_path = self.get_text_file_from_s3_bucket(s3_bucket, s3_key)
            self.words_with_counts = self.load_words()

    def load_words(self):
        words_with_counts = {}
        with open(self.file_path, "r") as file:
            for line in file:
                word, count = line.strip().split()
                words_with_counts[word] = int(count)
        return words_with_counts

    def get_text_file_locally(self):
        return self.file_path

    def get_words_with_counts(self):
        return self.words_with_counts

    def get_text_file_from_s3_bucket(self, bucket_name, object_key):
        s3_client = boto3.client("s3")
        local_file_name = object_key.split("/")[-1]
        s3_client.download_file(bucket_name, object_key, local_file_name)
        return local_file_name
